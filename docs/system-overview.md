# Tiketa System Blueprint

Tiketa is a cinematic time-capsule: every studio inside “The Time Gallery” screens exactly one film, forever, preserving a curated canon of masterpieces. The platform lets visitors browse studios, explore a film’s lore, watch its trailer, and reserve a seat in that film’s eternal run. This document explains **what the product stands for** and **how the software realizes it**, giving a new engineer everything needed to rebuild the system from scratch.

---

## 🎯 Product Concept — What & Why

| Aspect | Details |
| --- | --- |
| **Audience** | Film enthusiasts visiting a fictional premium cinema that celebrates iconic titles. |
| **Promise** | Each studio is dedicated to a single movie; screenings follow a predictable rhythm so fans can plan pilgrimages. |
| **Problems Solved** | Curated discovery (no content overload), tangible scheduling (every studio runs on rails), and effortless booking with visual seat selection. |
| **Experience Pillars** | Story-rich copy (“Now Showing, Forever”), high-gloss UI, responsive layouts, and immersive booking UX. |

---

## 🧰 Technology Stack — How It’s Built

| Layer | Technology | Purpose |
| --- | --- | --- |
| Language | Python 3.13 | Primary runtime for backend and scripts. |
| Web Framework | Flask 3.0 | App factory pattern with modular blueprints. |
| ORM | Flask-SQLAlchemy 3.1 over SQLAlchemy 2.0 | Entity modelling, relationship management, DB access. |
| Database | PostgreSQL (prod), SQLite (default dev) | Persistent storage for movies, showtimes, bookings, genres. |
| Config | python-dotenv 1.0 | Loads environment variables from `.env`. |
| Frontend | Jinja templates, semantic HTML5, bespoke CSS, Font Awesome icons | Server-rendered UI with dark neon aesthetic. |
| Scripting | `generate_schedule.py` | Maintains rolling showtime windows by archiving past slots and creating new ones. |

Dependencies are pinned in `requirements.txt`, ensuring reproducible environments.

---

## 🏗️ System Architecture — How Everything Fits

```mermaid
flowchart LR
     UserBrowser[(Browser)] -- HTTP --> Flask
     Flask -- imports --> AppFactory
     AppFactory -- configures --> Extensions[(SQLAlchemy, dotenv)]
     AppFactory -- registers --> MoviesBlueprint
     MoviesBlueprint -- renders --> Templates
     Templates -- read/write --> Database[(Movies, Genres, Showtimes, Bookings)]
     ScheduleScript{{generate_schedule.py}} -- app context --> Database
```

1. **Entry point**: `run.py` instantiates the Flask app via `create_app()` and honours `FLASK_DEBUG` and `PORT` toggles.
2. **App factory** (`app/__init__.py`):
    - Loads `.env`, configures secrets and database URI.
    - Boots SQLAlchemy, registers the `movies` blueprint.
    - On a pristine database, seeds 21 movies along with their genres and initial showtimes.
3. **Request flow**:
    - Routes in `app/movies/routes.py` handle listing, details, and booking.
    - Templates in `templates/` render responses and embed lightweight JavaScript for trailer modals and seat selection.
4. **Background maintenance**:
    - `generate_schedule.py` can be run manually or scheduled (cron/Task Scheduler). It archives past showtimes via a soft-delete flag and ensures 3 days of future screenings.

The application is intentionally stateless; all persistent state lives in the database. Session data uses Flask’s secure cookies.

---

## 🗂️ Repository Map — Where Things Live

```
tiketa-app/
├── run.py                   # WSGI entry point
├── generate_schedule.py     # Rolling schedule maintenance script
├── requirements.txt         # Locked Python dependencies
├── app/
│   ├── __init__.py          # Flask app factory, config, first-run seeding
│   ├── models.py            # SQLAlchemy models + association tables
│   ├── layouts.py           # Canonical cinema seat map definition
│   ├── movies/
│   │   ├── __init__.py      # Blueprint registration
│   │   └── routes.py        # All HTTP endpoints & booking logic
│   └── sample_data/
│       └── movies.py        # Curated film metadata and trailer IDs
├── templates/
│   ├── base.html            # Global HTML shell, styles, fonts, tokens
│   └── movies/
│       ├── index.html       # Studio catalog landing page
│       ├── detail.html      # Film detail, schedule, trailer modal
│       └── book.html        # Interactive seat reservation flow
├── docs/
│   └── system-overview.md   # This document
└── venvtiketa/              # (Optional) Pre-created virtual environment
```

Each folder is intentionally small: one blueprint, one seat-map helper, and a sample dataset the seeding routine can trust.

---

## 🧱 Core Components — Critical Building Blocks

### App Factory & Configuration (`app/__init__.py`)
- Loads environment variables using `python-dotenv`.
- Defines `create_app(config=None)` to support tests or alternate configs.
- Configures `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, and disables modification tracking for performance.
- Initializes SQLAlchemy and registers the `movies` blueprint.
- **First-run seeding**: if the `movies` table is empty, it iterates through `SAMPLE_MOVIES`, ensures matching `Genre` objects exist, and creates schedule slots based on studio parity.

### Data Model (`app/models.py`)
- `Movie`: unique `studio_number`, poster/backdrop paths, `trailer_youtube_id`, and `release_date`. Many-to-many `genres` through `movie_genres` association table. Has ordered `showtimes` relationship.
- `Genre`: canonical genre names, linked back to movies.
- `Showtime`: `time` stamp, foreign key to movie, `is_archived` soft-delete flag, and `created_at`. Relationship to `Booking` objects.
- `Booking`: captures `user`, `seat`, `showtime_id` with a unique constraint to prevent double-booking.

These models are small but expressive enough to describe the cinema, its schedule, and reservations.

### Seat Layout Helper (`app/layouts.py`)
- Exposes `SEAT_MAP`, an asymmetric auditorium grid using `None` sentinels for aisles and walkways.
- Keeps view logic clean by supplying a consistent structure the template can traverse.

### Movies Blueprint (`app/movies/routes.py`)
- `/`: Lists every movie ordered by studio, injecting metadata for the landing page cards.
- `/movie/<movie_id>`: Fetches one movie, gathers upcoming showtimes (next three days) excluding archived slots, groups them by date, and passes a `timedelta` helper for end-time calculations. Also exposes trailer IDs to the template.
- `/book/<showtime_id>`: On GET, renders the seating chart with current bookings; on POST, validates form inputs, enforces seat uniqueness, flashes status messages, and redirects back to reflect the new seat state.

### Template Layer (`templates/`)
- `base.html` embeds global CSS tokens, Google Fonts, Font Awesome icons, and the app chrome. Blocks `extra_head` and `scripts` give individual pages room to extend styles/behaviour.
- `movies/index.html` implements the brand story, feature grid, and responsive cards.
- `movies/detail.html` presents cinematic hero content, core metadata, computed schedule messaging, and a modal trailer player that auto-starts/stops the YouTube iframe.
- `movies/book.html` renders the seat grid with stateful buttons and lightweight JavaScript helpers (`selectSeat`, `showTaken`).

### Scheduling Script (`generate_schedule.py`)
- Invokes the app factory standalone, then calls:
  - `purge_past_showtimes()` to mark passed showtimes as archived.
  - `generate_upcoming_showtimes()` to populate gaps for the next three days without duplicating existing live schedules.
- Intended for periodic execution (cron, GitHub Actions, Windows Task Scheduler) to keep the timetable rolling forward.

---

## 🔄 Data Flow Explained

### 1. Browsing Studios
1. User hits `/`.
2. `routes.index()` queries all `Movie` rows ordered by `studio_number`.
3. Template renders cards with poster art, genre tags, and computed daily slot counts (6 for even studios, 5 for odd).

### 2. Exploring a Film
1. User selects a movie, requesting `/movie/<id>`.
2. Route fetches the `Movie`, calculates a 3-day horizon, and pulls non-archived `Showtime` entries within that window.
3. Showtimes are grouped by date and rendered with computed end-times. The trailer button opens a modal which injects the YouTube embed URL on demand and clears it on close.

### 3. Booking Seats
1. User navigates to `/book/<showtime_id>`.
2. GET route loads the seat map, pre-tags taken seats by comparing `Booking` records.
3. Client-side JS visually marks availability and writes the chosen seat into a hidden field.
4. On form submit, POST validates `user` and `seat`, checks for existing bookings, and either flashes an error or persists the reservation.
5. The user is redirected back; GET re-renders with the seat now flagged as taken.

### 4. Maintaining Schedules
1. Operator runs `python generate_schedule.py`.
2. Past showtimes flip `is_archived=True` to preserve history without deleting rows.
3. For each movie and each day in the rolling window, the script only creates new rows when that day has no active showtimes, preventing duplicates.

These flows share a single source of truth (the database) and lean on server rendering for simplicity and reliability.

---

## ⚙️ Configuration & Environment Variables

| Variable | Purpose | Default |
| --- | --- | --- |
| `SECRET_KEY` | Secures Flask sessions and CSRF tokens. | `dev-secret-key-change-in-production` |
| `DATABASE_URL` | SQLAlchemy connection string (PostgreSQL recommended). | `sqlite:///tiketa.db` |
| `FLASK_DEBUG` | Enables live reload and verbose errors when `true`. | `False` |
| `PORT` | Overrides default port used by `run.py`. | `5000` |

Optional: standard PostgreSQL URI syntax (`postgresql://user:pass@host:port/dbname`). Place overrides in a `.env` file at the project root; `python-dotenv` loads it automatically.

---

## 🛠️ Local Setup & Operations

Follow these steps on a fresh machine (PowerShell shown; translate to Bash as needed):

```powershell
# 1. Clone and enter the project
git clone <repository-url>
cd tiketa-app

# 2. (Optional) remove the committed virtual environment and create your own
Remove-Item -Recurse -Force venvtiketa -ErrorAction SilentlyContinue
python -m venv venv

# 3. Activate the environment
.\venv\Scripts\Activate.ps1

# 4. Install backend dependencies
pip install -r requirements.txt

# 5. Create or update your .env file
New-Item -Path .env -ItemType File -Force
notepad .env  # populate with the values shown below

# 6. Launch the development server (auto-seeds on first run)
python run.py
```

Recommended `.env` skeleton:

```dotenv
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///tiketa.db
FLASK_DEBUG=true
PORT=5000
```

`python run.py` creates `tiketa.db` (when using SQLite) and seeds the cinema catalog automatically. Visit `http://localhost:5000` to browse studios, explore trailers, and book seats.

To regenerate schedules or roll the window forward without restarting the web server, run:

```powershell
python generate_schedule.py
```

### Common Operations

- **Reset the database**: Stop the server, delete `tiketa.db` (SQLite) or drop all tables in PostgreSQL, then rerun `python run.py` to trigger reseeding.
- **Inspect data interactively**: Start a REPL with `python`, then:
  ```python
  from app import create_app
  from app.models import db, Movie, Showtime, Booking
  app = create_app()
  with app.app_context():
      print(Movie.query.count())
  ```
- **Clear stale bookings**: Inside an app context, call `Booking.query.delete()` followed by `db.session.commit()` to wipe all reservations (useful for demos).
- **Update the curated catalog**: Edit `app/sample_data/movies.py`, remove existing movies, and rerun the seeding workflow.

---

## ♻️ Extensibility & Next Steps

- Add user authentication and a personal ticket wallet for repeat visitors.
- Integrate payment processing and QR-code ticketing for real deployments.
- Expose a JSON/GraphQL API so kiosks or mobile apps can share the same backend.
- Automate `generate_schedule.py` via cron/Task Scheduler or convert it into a Flask CLI command.
- Introduce automated tests (unit + integration) covering booking collisions, schedule generation, and template rendering.

---

## ✅ Final Notes

Tiketa’s codebase is intentionally compact: a single blueprint, explicit data models, and richly crafted templates. With this document and the source tree side by side, a new developer can stand up the experience in minutes, extend it confidently, and keep “The Time Gallery” open for the next century of cinema.

