# Tiketa System Blueprint (2025 Edition)

Tiketa imagines **The Time Gallery**, a cinema complex where every studio is devoted to a single iconic film looping forever. Visitors browse the catalog, inspect lore-rich detail pages, watch trailers, and reserve specific seats for a chosen showtime. This document is the authoritative reference for how the platform works architecturally, functionally, and operationally. A reader should be able to reproduce the system end-to-end using the information below.

---

## 🎬 Product Snapshot

| Dimension | Details |
| --- | --- |
| **Audience** | Film aficionados and demo-goers exploring a premium curated cinema. |
| **Value Props** | Curated catalog (21 masterpieces), predictable show rhythms, interactive seat booking, plush futuristic UI crafted with bespoke CSS. |
| **Primary Flows** | Browse studios → inspect film detail + trailer → choose showtime → reserve a seat. |
| **Tone** | Narrative-rich Indonesian/English mix, “Now Showing, Forever” motif, neon-dark aesthetic. |

---

## 🧰 Technology Stack

| Layer | Technology | Notes |
| --- | --- | --- |
| Runtime | Python 3.13 | Verified via committed virtualenv and tooling. |
| Framework | Flask 3.0.0 | App factory + blueprints, CLI command surface. |
| ORM | Flask-SQLAlchemy 3.1.1 on SQLAlchemy 2.0.43 | Declarative models, explicit association table. |
| Database | SQLite (`DATABASE_URL` default) or PostgreSQL (prod) | Run-time switch by environment variable. |
| Config & Secrets | `python-dotenv` 1.0 | Loads `.env` automatically during import. |
| Timezone Support | `pytz` 2025.2 | Used during seeding to anchor Asia/Jakarta showtimes. |
| Frontend | Jinja2 templates, custom CSS, Font Awesome, minimal vanilla JS | Single layout file + feature-specific pages. |
| Job Scripts | `generate_schedule.py`, `reset.py`, Flask CLI commands | Handle maintenance and data loading. |
| Dependencies | `requirements.txt` pinned versions | Recreate identical environment reliably. |

---

## 🏛️ Architecture Overview

```mermaid
flowchart TD
	Browser[(User Browser)] -- HTTP --> FlaskApp
	subgraph Application
		FlaskApp[/run.py\ncreate_app()/]
		AppFactory[/app/__init__.py/]
		MoviesBP[/app/movies/routes.py/]
		Templates[/templates/*.html/]
		Models[/app/models.py/]
		SeatMap[/app/layouts.py/]
	end
	subgraph Database
		Movies[(movies)]
		Genres[(genres)]
		Showtimes[(showtimes)]
		Bookings[(bookings)]
		movie_genres[(movie_genres)]
	end
	subgraph Maintenance
		ScheduleScript{{generate_schedule.py}}
		ResetScript{{reset.py}}
		SeedCLI{{flask seed-db}}
	end

	FlaskApp --> AppFactory
	AppFactory --> Models
	AppFactory --> MoviesBP
	MoviesBP --> Templates
	Templates --> Browser
	Models <--> Database
	SeatMap --> Templates
	ScheduleScript --> Database
	ResetScript --> Database
	SeedCLI --> Database
```

**Execution lifecycle**

1. `run.py` imports `create_app()` and starts Flask using `FLASK_DEBUG` and `PORT` toggles.
2. `create_app()` configures secrets and database URI, initializes SQLAlchemy, registers the movies blueprint, and ensures tables exist (`db.create_all()`).
3. Seeding is opt-in via CLI: `flask seed-db` runs `seed_initial_data()` to load curated movies and day-one showtimes.
4. Routes render Jinja templates that drive all UX. JavaScript is limited to trailer modals and seat picker helpers.
5. Maintenance scripts (`reset.py`, `generate_schedule.py`) operate inside an app context to manage data lifecycle.

---

## 📦 Repository Map

```
tiketa-app/
├── run.py                  # WSGI/CLI entry point (app + Flask commands)
├── generate_schedule.py    # Rolling showtime maintenance script
├── reset.py                # Helper to drop & recreate schema
├── requirements.txt        # Locked dependency versions
├── app/
│   ├── __init__.py         # App factory + seed_initial_data()
│   ├── models.py           # SQLAlchemy models & association table
│   ├── layouts.py          # Auditorium seat layout grid
│   ├── movies/
│   │   ├── __init__.py     # Blueprint factory
│   │   └── routes.py       # Browse, detail, booking endpoints
│   └── sample_data/
│       └── movies.py       # 21 curated movie definitions
├── templates/
│   ├── base.html           # Global shell & design tokens
│   └── movies/
│       ├── index.html      # Catalog landing page
│       ├── detail.html     # Film detail + trailer modal
│       └── book.html       # Seat selection + booking form
├── docs/
│   └── system-overview.md  # This document
└── venvtiketa/             # (Optional) committed virtualenv snapshot
```

---

## 🧱 Data Model

| Table | Purpose | Key Columns | Notable Constraints |
| --- | --- | --- | --- |
| `movies` | Master catalog, one per studio | `studio_number` (unique), `title`, `release_date`, artwork URLs, `trailer_youtube_id` | `studio_number` unique, genres via association table, `showtimes` relationship ordered by time. |
| `genres` | Canonical genre list | `name` | `name` unique; bidirectional many-to-many with movies. |
| `movie_genres` | Join table | `movie_id`, `genre_id` | Composite primary key ensures uniqueness. |
| `showtimes` | Individual screening slots | `movie_id`, `time`, `is_archived` | Soft delete via `is_archived`; `bookings` backref. |
| `bookings` | Seat reservations | `user`, `seat`, `showtime_id` | Unique constraint `uq_booking_showtime_seat` prevents double-booking same seat + showtime. |

All timestamps default to `datetime.utcnow()` when not supplied. Timezone-aware datetimes from `seed_initial_data()` (Asia/Jakarta) are stored directly; SQLAlchemy retains them (SQLite stores as ISO strings, PostgreSQL as `TIMESTAMP WITH TIME ZONE`).

---

## 🎟️ Seat Layout

`app/layouts.py` exports `SEAT_MAP`, a two-dimensional grid consumed by templates:

* Rows **A–J**: full-width with 18 seats each and an aisle between columns 9 and 10.
* Row **K**: walkway (entire row of `None`) rendered as a divider.
* Rows **L–M**: narrower tail rows.
* `None` entries mark aisles or walkways; templates render them as non-interactive gaps.

Templates rely on the grid to determine CSS layout and apply seat state (available, selected, taken). Seat IDs are persisted verbatim in bookings.

---

## 🌐 Request & UX Flows

### 1. Browse Catalog (`/`)
1. `routes.index()` fetches all movies ordered by studio.
2. Template shows hero copy, responsive cards, poster art, studio chip, genre tags, and implicit daily slot count (`6` for even studios, `5` for odd).
3. CTAs route to the detail page for deeper exploration.

### 2. Inspect a Film (`/movie/<movie_id>`)
1. Loads the target movie or 404s if missing.
2. Defines a three-day horizon: now → (today + 2 days, 23:59).
3. Queries non-archived showtimes in that window, groups them by date, and sorts chronologically.
4. Template renders cinematic hero layout, metadata, and trailer button. Trailer modal is hydrated client-side: open attaches the YouTube embed, closing wipes `src` to stop playback.

### 3. Reserve a Seat (`/book/<showtime_id>`, GET/POST)
1. GET: builds seat grid and marks taken seats using existing `Booking` rows for the showtime.
2. Client selects a seat; lightweight JS toggles CSS classes and writes to a hidden input.
3. POST: validates `user` and `seat`, checks for duplicates, creates a `Booking`, commits, and flashes a localized success message. Duplicate seats flash an error.
4. Redirect back to GET to reflect updated seat occupancy.

Flash messaging leverages Flask’s category mechanism. Templates localize certain strings to Bahasa Indonesia to fit the brand voice.

---

## 🧩 Templates & Frontend Behaviour

* `base.html` supplies fonts, color tokens, buttons, and shared layout. Footer renders static copy for 2025.
* `movies/index.html` emphasises marketing copy, handles studio parity messaging, and ensures cards remain responsive.
* `movies/detail.html` hosts the trailer modal logic, showtime list, and computed end-time (assumed 2h duration using `timedelta(hours=2)`).
* `movies/book.html` renders the seat picker, seat legend, and submission form. JS functions `selectSeat()` and `showTaken()` manage interactivity.

No build tooling is required; the frontend is server-rendered with inline CSS/JS designed for a small-scale demo.

---

## 🛠️ Maintenance Scripts & CLI

### Seeding (`seed_initial_data()`)
* Lives in `app/__init__.py`.
* Checks if `Movie.query.count() == 0` before inserting.
* Pulls 21 curated records from `app/sample_data/movies.py`.
* For each movie: creates `Movie`, attaches/creates `Genre` rows, generates daily showtimes using timezone-aware `Asia/Jakarta` datetimes.
* Slots follow parity rules (even studio → 6 slots every 3 hours starting 06:00; odd studio → 5 slots every 4 hours).
* Invocation is manual via CLI to avoid unintended duplicate data.

### Flask CLI Commands (`run.py`)
* `flask reset-db` — Drop and recreate all tables (no seeding).
* `flask seed-db` — Run `seed_initial_data()`; safe to call repeatedly (no-op if movies already present).

### `reset.py`
Standalone helper mirroring `flask reset-db`. Useful when Flask CLI is not configured; simply runs `db.drop_all()` followed by `db.create_all()`.

### `generate_schedule.py`
* Purges past showtimes by setting `is_archived=True` for slots starting before today (`time.min`).
* For the next `days` (default 3), checks **per movie + day** if any live showtime exists. If none, it creates a fresh batch using parity rules and a starting time of 07:00 local.
* Returns counts of purged and created records; prints summary when run standalone.
* Intended for cron/Task Scheduler to keep the schedule rolling without restarting the web server.

> ⚠️ Because showtimes created during seeding use Asia/Jakarta timezone-aware datetimes, ensure the database engine handles timezone consistently. SQLite stores them as strings; PostgreSQL will normalise to UTC while preserving offsets.

---

## ⚙️ Configuration & Environment

| Variable | Default | Description |
| --- | --- | --- |
| `SECRET_KEY` | `dev-secret-key-change-in-production` | Flask session + CSRF signing key. Override in production. |
| `DATABASE_URL` | `sqlite:///tiketa.db` | SQLAlchemy connection string; supports PostgreSQL, SQLite, etc. |
| `FLASK_DEBUG` | `False` | Enables debug server when set to `true`. |
| `PORT` | `5000` | Port used by `python run.py`. |

Configuration is loaded via `python-dotenv`; place overrides in a `.env` file at the project root.

---

## 🧪 Local Development Playbook (PowerShell)

```powershell
# 1. Clone and enter the project
git clone <repository-url>
cd tiketa-app

# 2. (Optional) remove the committed virtualenv and create a fresh one
Remove-Item -Recurse -Force venvtiketa -ErrorAction SilentlyContinue
python -m venv .venv

# 3. Activate the environment
.\.venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
Copy-Item .env.example .env -ErrorAction SilentlyContinue
# or create manually:
# Set-Content .env @'
# SECRET_KEY=dev-secret-key-change-in-production
# DATABASE_URL=sqlite:///tiketa.db
# FLASK_DEBUG=true
# PORT=5000
# '@

# 6. Create schema
flask --app run.py reset-db

# 7. Seed curated catalog (idempotent)
flask --app run.py seed-db

# 8. Launch the server
python run.py

# Optional: refresh rolling showtimes
python generate_schedule.py
```

Visit `http://localhost:5000` to browse the cinema. The first server launch will use the seeded data; subsequent launches read persisted records from `tiketa.db` (or the configured database).

---

## 🗃️ Sample Data Reference

* File: `app/sample_data/movies.py`
* Contains 21 entries with studio numbers 1–21, each with description, release date, poster/backdrop URLs, YouTube trailer IDs, and genre list.
* Genres align with the curated set defined during seeding; duplicates are deduplicated at insert time.
* Update this file to modify the canon, then re-run `flask seed-db` after resetting the database.

---

## 🔄 Operational Guidelines

| Scenario | Action |
| --- | --- |
| **Reset database** | `flask --app run.py reset-db` or `python reset.py` |
| **Reseed curated data** | `flask --app run.py seed-db` |
| **Roll schedule forward** | `python generate_schedule.py` (can be scheduled) |
| **Inspect data manually** | Launch Python shell → `from app import create_app; from app.models import db, Movie; app = create_app(); app.app_context().push(); Movie.query.count()` |
| **Switch to PostgreSQL** | Update `.env` `DATABASE_URL=postgresql://user:pass@host:port/db`; rerun reset + seed commands. |

---

## 🚧 Limitations & Considerations

* No authentication, payments, or inventory caps beyond seat uniqueness.
* Show durations are hard-coded to 2 hours and not stored in the database.
* Timezone handling mixes aware (seeding) and naive (runtime queries). When running outside Asia/Jakarta, ensure server timezone assumptions are documented.
* There are no automated tests; manual validation is required after changes.
* Frontend assets are inline; large-scale theming would benefit from CSS modularisation.

---

## 📈 Extensibility Ideas

1. Add user accounts and history of bookings per user.
2. Attach film runtime to `Movie` and compute end-times accurately.
3. Convert `generate_schedule.py` into a Flask CLI command and parameterise horizon length.
4. Introduce REST/GraphQL APIs for kiosk or mobile integrations.
5. Implement automated tests for booking collisions, schedule generation, and template rendering.
6. Externalise seat maps per studio in the database to support varied auditorium layouts.

---

## ✅ Summary

Tiketa is a self-contained Flask application showcasing a cinematic booking flow with handcrafted UI, deterministic showtime logic, and clear operational scripts. This blueprint documents every component—from data schema and request handling to maintenance utilities—so engineers and AI agents alike can rebuild, extend, or deploy the system with confidence.

