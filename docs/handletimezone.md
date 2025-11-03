# Timezone handling in Tiketa (UTC ⇄ UTC+7 / Asia/Jakarta)

Dokumen ini menjelaskan secara lengkap dan detil bagaimana sistem Tiketa saat ini meng-handle waktu (UTC dan UTC+7 / Asia/Jakarta), dari sisi model, seeding/generator jadwal, routes, template, dan cleanup/archiving. Termasuk analisis logika, contoh-contoh konversi, potensi masalah, dan rekomendasi perbaikan.

---

## Ringkasan singkat (intisari)

- Penyimpanan di database: kolom `Showtime.time` menggunakan `DateTime` tanpa atribut timezone. Nilainya disimpan sebagai "naive UTC" (datetime tanpa tzinfo, tetapi berisi waktu UTC).
- Pembuatan jadwal / seeding: sistem membuat waktu dalam zona `Asia/Jakarta` (WIB), kemudian mengonversi ke UTC dan menyimpan hasilnya sebagai naive UTC.
- Scheduler (`generate_schedule.py`) dan seeding (`app/__init__.py`) menggunakan `pytz` dan helper yang mengembalikan nilai-naive saat menyimpan ke DB.
- Saat membaca untuk ditampilkan di UI, route mengonversi dari naive UTC yang ada di DB ke Jakarta-time untuk tampilan. Template menampilkan `showtime.local_start` / `local_end` yang diberikan oleh route.
- Purge/archive: perbandingan waktu juga dilakukan menggunakan naive UTC (mis. `datetime.utcnow().replace(tzinfo=None)`) sehingga cocok membandingkan dengan kolom `time` yang juga naive UTC.

Dokumen ini akan menjabarkan detail per-file, contoh konversi, masalah potensial, dan rekomendasi implementasi yang lebih aman.

---

## Dokumen per-file: apa yang terjadi dan bagaimana cara kerjanya

Saya merangkum lokasi kode penting dan apa yang dilakukan.

### 1) Model: `app/models.py`

- `Showtime.time` didefinisikan sebagai `db.Column(db.DateTime, nullable=False)`.
- Artinya: kolom DB menyimpan `datetime` tanpa informasi timezone (naive).
- Konsekuensi saat ini: semua nilai yang disimpan oleh aplikasi harus konsisten (mis. selalu menyimpan UTC, atau selalu menyimpan lokal) agar perbandingan dan query benar. Proyek ini memilih menyimpan "UTC, tapi sebagai naive".

Relevan snippet (ringkasan):

- `class Showtime` memiliki `time = db.Column(db.DateTime, nullable=False)`

### 2) Seeding: `app/__init__.py` (`seed_initial_data`)

- Fungsi `seed_initial_data()` menggunakan `pytz.timezone('Asia/Jakarta')` untuk membuat waktu lokal Jakarta.
- Terdapat helper `to_utc_naive(local_dt: datetime) -> datetime` yang:
  - menerima datetime lokal (sebagai naive pada saat `first_show_datetime()` dikembalikan),
  - melakukan `local_aware = jakarta_tz.localize(local_dt)`,
  - mengubah timezone: `local_aware.astimezone(pytz.UTC)`,
  - kemudian `replace(tzinfo=None)` untuk menghasilkan naive UTC datetime.
- Saat menambahkan `Showtime(...)`, yang disimpan adalah `show_time_utc` — hasil `to_utc_naive`, yaitu naive UTC.

Singkatnya: seeding membuat waktu local (Jakarta) -> localize (aware) -> konversi ke UTC -> drop tzinfo -> simpan.

### 3) Generator jadwal & maintenance: `generate_schedule.py`

- File ini adalah script untuk memastikan ada jadwal 3 hari ke depan.
- Menggunakan `pytz.timezone('Asia/Jakarta')` (dideklarasikan `JAKARTA_TZ`), `UTC = pytz.UTC`.
- Ada helper utama:
  - `_to_utc_naive(local_dt)` — menerima `local_dt` (naive or aware Jakarta-local) dan mengembalikan naive UTC (localize jika perlu, astimezone(UTC), replace(tzinfo=None)).
  - `_to_local_naive(utc_dt)` — menerima naive UTC (atau aware) lalu mengembalikan naive Jakarta-local (UTC.localize(...).astimezone(JAKARTA_TZ).replace(tzinfo=None)).
- Logic:
  - `generate_upcoming_showtimes` membentuk jam-jam yang diharapkan berdasarkan lokal (contoh start jam 06:00 WIB), lalu memanggil `_to_utc_naive` untuk menyimpan ke DB.
  - Saat membandingkan existing showtimes, script menormalisasi koleksi existing ke bentuk lokal (set of naive local datetimes) dengan `_to_local_naive` sehingga bisa dibandingkan dengan expected local times.
- `purge_past_showtimes()` menggunakan `_now_utc_naive()` yang mengembalikan `datetime.utcnow().replace(tzinfo=None)` — dibandingkan langsung dengan kolom `Showtime.time` (naive UTC) untuk menandai `is_archived=True`.

Inti: generate_schedule membuat/menyimpan UTC-naive dan juga dapat mengubah kembali ke lokal-naive untuk perhitungan.

### 4) Routes / tampilan: `app/movies/routes.py`

- Routes mendefinisikan `JAKARTA_TZ = pytz.timezone('Asia/Jakarta')` dan `UTC = pytz.UTC`.
- Helper:
  - `_utc_naive(dt: datetime) -> datetime`: melakukan `dt.astimezone(UTC).replace(tzinfo=None)` — digunakan untuk membuat boundary `start_utc` dan `end_utc` ketika query showtimes.
  - `_to_local(dt_utc_naive: datetime) -> datetime`: melakukan `UTC.localize(dt_utc_naive).astimezone(JAKARTA_TZ)` — mengembalikan *aware* Jakarta datetime (tidak di-`.replace(tzinfo=None)`), sehingga nilai yang dipakai di template (`showtime.local_start`) adalah aware (memiliki tzinfo Asia/Jakarta).
- Contoh alur pada `movie_detail`:
  1. buat `now_local = datetime.now(JAKARTA_TZ)` (aware)
  2. `horizon_local = JAKARTA_TZ.localize(horizon_local)` (aware)
  3. `start_utc = _utc_naive(now_local)` — ini akan menghasilkan naive UTC untuk dipakai di query
  4. ambil `Showtime` antara `start_utc` dan `end_utc` (keduanya naive UTC),
  5. untuk setiap showtime dari DB (naive UTC), lakukan `local_start = _to_local(showtime.time)` → hasil aware Jakarta timezone — simpan ke `showtime.local_start` untuk template.

- Pada `book_ticket` route: saat GET/POST, `showtime.local_start = _to_local(showtime.time)` juga dilakukan; template `book.html` mencetak `.local_start.strftime(...)` (yang aman karena aware Jakarta datetime).

### 5) Templates: `templates/movies/detail.html` dan `book.html`

- Templates mengharapkan `showtime.local_start` dan `showtime.local_end` sudah disiapkan di route.
- Contoh tampilan: `{{ showtime.local_start.strftime('%H:%M') }}` dan `{{ showtime.local_start.strftime('%A, %B %d, %Y at %I:%M %p') }}`.
- Karena route mengisi `local_start` sebagai Jakarta-aware datetime (dari `_to_local`), formatting untuk tampilan lokal bekerja benar.

---

## Contoh alur konversi (kasus nyata)

Misal kita ingin menyimpan showtime untuk 8:00 WIB (Jakarta) pada 2025-10-28.

1. Seeding / scheduler membuat `datetime(2025,10,28,8,0)` sebagai naive local (tidak ada tzinfo).
2. Dipanggil `to_utc_naive(local_dt)` atau `_to_utc_naive(local_dt)`:
   - `local_aware = jakarta_tz.localize(local_dt)` → hasil: 2025-10-28 08:00+07:00
   - `local_aware.astimezone(pytz.UTC)` → hasil: 2025-10-28 01:00+00:00
   - `.replace(tzinfo=None)` → hasil yang disimpan: 2025-10-28 01:00 (naive)
3. DB menyimpan `Showtime.time = 2025-10-28 01:00` (anggap DB tanpa tz)

Saat user melihat halaman:
1. Route ambil showtime.time (naive UTC 2025-10-28 01:00)
2. `_to_local(naive_utc)` melakukan `UTC.localize(naive_utc).astimezone(JAKARTA_TZ)` → hasil: 2025-10-28 08:00+07:00 (aware)
3. Template menampilkan `08:00` / tanggal di zona Jakarta.

---

## Konsistensi & potensi masalah (detail teknis)

Saya mencatat beberapa area yang bisa berpotensi menimbulkan bug atau kebingungan:

1. Mix of naive vs aware datetimes
   - Proyek saat ini menyimpan `datetime` tanpa tzinfo (naive) di DB, tetapi "saat berpikir" dalam kode sering berganti-ganti antara aware dan naive.
   - Contoh: seeding -> `to_utc_naive` menghasilkan naive UTC. Scheduler `_to_local_naive` menghasilkan naive local. Routes menggunakan `_to_local` yang mengembalikan aware local.
   - Meski secara praktis ini "bekerja" jika semua konversi dilakukan konsisten (selalu menyimpan UTC sebagai naive), kombinasi naive/aware berisiko bila ada fungsi yang lupa melakukan localize/astimezone dengan benar.

2. Penggunaan `pytz` dan `.localize()`
   - Kode menggunakan `pytz` dan metode `.localize()` (benar untuk `pytz`) namun `pytz` memiliki pola penggunaan berbeda dibanding `zoneinfo` (PEP 615). Interaksi `replace(tzinfo=None)` harus dilakukan hati-hati.

3. DST & edge-cases
   - Indonesia (Asia/Jakarta) tidak menerapkan DST, sehingga risiko DST kecil di sini. Namun, jika sebuah server berpindah zona atau developer menguji dari zona lain, masalah bisa muncul.

4. Database column tidak bertipe timezone-aware
   - `db.DateTime` tanpa argumen `timezone=True` membuat kolom tidak menyimpan zona secara native. Kecuali Anda yakin selalu menyimpan UTC dan selalu membaca sebagai UTC, ini berisiko untuk developer lain.

5. Query comparisons are done with naive UTC
   - `purge_past_showtimes()` menggunakan `datetime.utcnow().replace(tzinfo=None)` dan membandingkannya ke `Showtime.time` — ini konsisten dengan penyimpanan saat ini (naive UTC). Namun jika nanti kolom DB diubah menjadi timezone-aware, query perlu disesuaikan.

6. Minor inconsistencies across codebase
   - `app/__init__.py` dan `generate_schedule.py` menggunakan slightly different helpers (`to_utc_naive` vs `_to_utc_naive`, `_to_local_naive`), beberapa mengembalikan naive local, beberapa mengembalikan aware local.

---

## Rekomendasi perubahan (implementasi yang lebih aman dan maintainable)

Jika Anda ingin meningkatkan keamanan dan mengurangi risiko bug, pertimbangkan perubahan ini (dengan langkah migrasi):

1. Simpan semua waktu di DB sebagai UTC *aware* (dengan tzinfo=UTC) dan gunakan kolom SQLAlchemy `DateTime(timezone=True)`.
   - Keuntungan: jelas secara semantik, SQL engines (Postgres) bisa menyimpan timezone-aware types. Mengurangi kebutuhan untuk `.replace(tzinfo=None)`.
   - Migration: untuk SQLite yang tidak menyimpan timezone, simpan string ISOformat atau tetap naive UTC tetapi dokumen internal menyatakan "value is UTC". Untuk Postgres, alter column to timestamptz.

Contoh perubahan pada model:

```python
# app/models.py (snippet)
from sqlalchemy.sql import func

class Showtime(db.Model):
    # ...
    # make timezone-aware
    time = db.Column(db.DateTime(timezone=True), nullable=False)
```

2. Buat modul helper timezone terpusat (single source of truth), misal `app/timezone.py` dengan API kecil:

- now_utc() -> datetime aware UTC
- now_local() -> datetime aware Jakarta
- to_utc(dt: datetime) -> datetime aware UTC (jika naive, asumsi: local Jakarta or input param?)
- to_local(dt: datetime, tz_name: str = 'Asia/Jakarta') -> datetime aware local
- to_utc_naive(dt: datetime) -> datetime naive UTC (opsional, jika Anda ingin tetap menyimpan naive)

Contoh implementasi (menggunakan pytz untuk kompatibilitas dengan codebase saat ini):

```python
# app/timezone.py
from datetime import datetime
import pytz

JAKARTA = pytz.timezone('Asia/Jakarta')
UTC = pytz.UTC

def now_utc() -> datetime:
    return datetime.now(UTC)

def now_local() -> datetime:
    return datetime.now(JAKARTA)

def to_aware_utc(dt: datetime) -> datetime:
    # If naive, assume it's local Jakarta; otherwise convert
    if dt.tzinfo is None:
        dt = JAKARTA.localize(dt)
    return dt.astimezone(UTC)

def to_aware_local(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        # assume dt is UTC naive
        dt = UTC.localize(dt)
    return dt.astimezone(JAKARTA)
```

3. Standardisasi return types
   - Pilih: "always return aware datetimes in code" adalah pilihan yang paling aman.
   - Jika Anda harus support SQLite/legacy naive DB fields, buat wrapper untuk membaca DB value and immediately convert to aware: `db_val = row.time` → `if db_val.tzinfo is None: db_val = db_val.replace(tzinfo=UTC)`.

4. Adjust query code when switching to timezone-aware columns
   - SQLAlchemy+Postgres: when column is `DateTime(timezone=True)` you can pass aware datetime objects directly in filters.
   - For SQLite, continue storing naive UTC but maintain conversion helpers so code still gets aware datetimes.

5. Replace `pytz` with stdlib `zoneinfo` (optional but recommended for modern code)
   - `zoneinfo` API is more idiomatic: `from zoneinfo import ZoneInfo` and `dt.replace(tzinfo=ZoneInfo('Asia/Jakarta'))` or `dt.astimezone(ZoneInfo('UTC'))`.
   - Note: when porting from `pytz`, be careful: `pytz.localize()` behaviour differs subtly from `replace(tzinfo=...)`.

6. Add unit tests / property-based tests for conversions
   - Test conversions round-trip: local -> utc -> local matches expected
   - Test purge logic with frozen time (freezegun) / test harness

---

## Migration steps (contoh langkah praktis)

Jika Anda memutuskan untuk switch ke timezone-aware storage (Postgres timestamptz), langkah ringkas:

1. Add new column `time_tz timestamptz NULL`.
2. Run a script that iterates over existing rows:
   - read `time` (naive, assumed UTC), convert to aware UTC: `UTC.localize(time)` or `time.replace(tzinfo=UTC)`, then write to `time_tz`.
3. Update model to use `time_tz` as `time = db.Column(db.DateTime(timezone=True))` and migrate data (rename column, drop old one).
4. Update all code paths to use aware datetimes (helpers in `app/timezone.py`), and remove `.replace(tzinfo=None)` calls used to keep naive storage.
5. Run test-suite.

Jika menggunakan SQLite and you cannot set timezone-aware column, keep storing naive UTC but make sure all code converts quickly to aware after reading.

---

## Quick checklist to verify current system correctness

- [x] Seeding & generator convert Jakarta -> UTC before saving (ya, ada helper `to_utc_naive` / `_to_utc_naive`).
- [x] Routes convert UTC -> Jakarta before display (ya, `_to_local` ada dan route mengisinya ke showtime.local_start).
- [x] Purge logic compares UTC-now to DB value using naive UTC (sesuai dengan current storage) — ini konsisten.
- [ ] Konsistensi return types across helpers (perlu perbaikan: beberapa helper mengembalikan naive, satu mengembalikan aware).

---

## Contoh perbaikan kode (minimal, non-disruptive)

Jika Anda ingin perubahan kecil yang meminimalkan perubahan DB tetapi membuat kode lebih konsisten, lakukan:

1. Buat `app/timezone.py` dan pakai helper untuk semua konversi.
2. Pastikan semua helper mengembalikan `aware` ketika dipakai oleh kode tampilan. Jika ingin tetap menyimpan naive UTC di DB, lakukan `.astimezone(UTC).replace(tzinfo=None)` hanya di lapisan penyimpanan.

Contoh `app/timezone.py` lebih lengkap (pytz-based):

```python
# app/timezone.py
from datetime import datetime
import pytz

JAKARTA = pytz.timezone('Asia/Jakarta')
UTC = pytz.UTC

def to_db_utc_naive(local_dt: datetime) -> datetime:
    """Convert local Jakarta (naive or aware) to naive UTC for storage."""
    if local_dt.tzinfo is None:
        local_dt = JAKARTA.localize(local_dt)
    return local_dt.astimezone(UTC).replace(tzinfo=None)

def from_db_utc_naive_to_aware_local(utc_dt: datetime) -> datetime:
    """Convert naive-UTC from DB to aware Jakarta datetime for display."""
    if utc_dt.tzinfo is None:
        utc_dt = UTC.localize(utc_dt)
    return utc_dt.astimezone(JAKARTA)

def now_utc_naive() -> datetime:
    return datetime.utcnow().replace(tzinfo=None)

def now_aware_utc() -> datetime:
    return datetime.now(UTC)
```

Ganti pemanggilan langsung ke `pytz` di beberapa file dengan helper ini.

---

## Testing & verification

- Unit test ideas:
  - Test `to_db_utc_naive(datetime(2025,10,28,8,0)) == datetime(2025,10,28,1,0)` (naive UTC)
  - Test `from_db_utc_naive_to_aware_local(datetime(2025,10,28,1,0)).tzinfo` adalah Jakarta tzinfo dan hour == 8
  - Test `purge_past_showtimes()` archives showtimes whose `time` < `now_utc_naive()`

- Manual smoke test (dev machine):
  - Run seeding (if DB empty) and confirm in DB that `showtimes.time` values correspond to expected UTC times.
  - Start app, visit a movie detail page and confirm displayed times match Jakarta local schedule.

---

## Summary dan rekomendasi prioritas

- Saat ini sistem berfungsi dengan pola: create local Jakarta → convert to UTC → save as naive UTC → read naive UTC → convert to aware Jakarta → display.
- Ini adalah pola yang valid dan relatif sederhana, tetapi ada inkonsistensi return types dan tersebarnya helper konversi.
- Prioritas perbaikan (rekomen):
  1. Buat helper timezone terpusat (`app/timezone.py`) dan gunakan di seluruh codebase.
  2. Konsistenkan return types: prefer menggunakan `aware datetimes` di lapisan aplikasi; hanya convert ke naive saat menulis ke DB jika DB tidak menangani timezone.
  3. Jika menggunakan Postgres, ubah kolom ke `DateTime(timezone=True)` dan simpan aware UTC.
  4. Tambahkan unit tests untuk semua helper konversi dan behaviour purge/generate.

---

Jika Anda mau, saya bisa:

- Menambahkan file helper `app/timezone.py` dan mengganti pemakaian helper di `generate_schedule.py` + `app/__init__.py` + `app/movies/routes.py` sedikit demi sedikit (patch minimal).
- Atau, langsung mengubah model `Showtime.time` menjadi timezone-aware dan membuat skrip migrasi.

Beritahu saya, mana yang ingin Anda prioritas: perbaikan kecil (helper terpusat) atau migrasi ke timezone-aware DB?