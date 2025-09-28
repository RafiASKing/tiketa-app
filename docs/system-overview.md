# Tiketa System Overview

This document captures the current architecture, data model, and user experience of the Tiketa cinema booking platform. It reflects all refinements completed during the recent development cycle, including the expanded movie roster, studio scheduling rules, and upgraded booking interface.

## Platform Snapshot

- **Framework**: Flask 3 with the application factory pattern and blueprint modularity
- **Data Layer**: SQLAlchemy ORM targeting PostgreSQL in production with SQLite fallback for local runs
- **Runtime Entry**: `run.py` bootstraps the factory-created app and honours `FLASK_DEBUG` / `PORT`
- **Domain Scope**: MegaCinema Bekasi with 21 permanent studios, each dedicated to a single film
- **UI Stack**: Server-rendered Jinja templates styled with modern CSS, gradients, and responsive layout primitives

## High-Level Topology

```
run.py (entry)
└── app.create_app()
    ├── Configuration (SECRET_KEY, DATABASE_URL, SQLAlchemy)
    ├── Database initialisation + seeding
    └── Blueprint registration
        └── movies blueprint (`/`, `/movie/<id>`, `/book/<showtime_id>`)
```

Request handling follows the canonical Flask lifecycle:

1. `run.py` imports `create_app()` and launches the WSGI server.
2. `create_app()` wires configuration, initialises the SQLAlchemy extension, and registers the movies blueprint.
3. On first boot, the seeding routine inserts movies, showtimes, and derived scheduling data.
4. Routes render Jinja templates or persist bookings, returning HTML responses.

## Data Model

The ORM schema resides in `app/models.py` and contains three core entities.

| Model | Key Fields | Notes |
| --- | --- | --- |
| `Movie` | `title`, `description`, `studio_number`, metadata fields | One movie per studio (`studio_number` unique). Holds poster, genres, release date. |
| `Showtime` | `movie_id`, `time` | Linked to `Movie`; stores scheduled screening start. |
| `Booking` | `user`, `seat`, `showtime_id` | Unique constraint per (`showtime_id`, `seat`) prevents double booking. |

Relationships:

- `Movie.showtimes` (1→many) yields ordered screenings via `order_by='Showtime.time'`.
- `Showtime.bookings` (1→many) gathers bookings for seat-map hydration.

Timestamps (`created_at`) are stored for auditing and display in the booking UI.

## Seeding & Scheduling Rules

The database seeding process runs inside the app context the first time the tables are empty:

1. Load `SAMPLE_MOVIES` from `app/sample_data/movies.py` (21 curated titles mapped to studio numbers).
2. Compute the next available start time at 06:00.
3. Generate a studio-specific schedule:
   - **Even-numbered studios** get 6 daily slots spaced every 3 hours.
   - **Odd-numbered studios** get 5 daily slots spaced every 4 hours.
4. Persist each movie and its generated showtimes in a single transaction.

The resulting calendar ensures every studio runs a single film indefinitely while preserving cadence variety between odd and even auditoriums.

## Route & View Behaviour

All HTTP endpoints live in `app/movies/routes.py` under the `movies` blueprint.

| Route | Method(s) | Purpose |
| --- | --- | --- |
| `/` | GET | List all movies ordered by studio with hero messaging and genre tags. |
| `/movie/<int:movie_id>` | GET | Show detail page with poster, metadata, and showtimes. |
| `/book/<int:showtime_id>` | GET/POST | Render interactive seating chart, accept booking submissions, flash status. |

Booking posts validate both the patron name and seat selection, enforce seat uniqueness, and redirect back to the same page on success so the refreshed seat map reflects the new reservation instantly.

## Template Layer & UX Highlights

Templates share the `base.html` shell that defines the glassmorphism aesthetic, header nav, and inline design tokens. Feature highlights:

- **Index (`movies/index.html`)**: Hero copy, responsive movie cards, studio chips mirroring odd/even scheduling, consistent poster source via remote CDN.
- **Detail (`movies/detail.html`)**: Large poster presentation, genre badges, dynamic slot count messaging (`5` vs `6` shows per day), and computed end-times using `timedelta`.
- **Book (`movies/book.html`)**: Seat grid (A–E × 1–10) with colour-coded states, inline JavaScript for selection feedback, and alerting for already reserved seats.

All templates rely on the central design palette declared in `base.html`, ensuring the UI shifts cohesively across viewport sizes.

## Configuration & Environment

Key environment variables consumed by `create_app()`:

- `SECRET_KEY` — session security (falls back to a development sentinel value).
- `DATABASE_URL` — SQLAlchemy connection string; PostgreSQL preferred, SQLite fallback.
- `FLASK_DEBUG`, `PORT` — optional runtime knobs respected by `run.py`.

`.env` files are supported through `python-dotenv`, allowing local overrides without code changes.

## Local Development Workflow

1. Create and activate a Python 3.13 virtual environment (the repository ships with `venvtiketa/` but you can recreate it).
2. Install dependencies via `pip install -r requirements.txt`.
3. Ensure the target database is reachable (for SQLite nothing is required).
4. Launch the server with `python run.py`; initial start will seed the sample dataset automatically.
5. Visit `http://localhost:5000/` to browse listings, inspect detail pages, and submit seat reservations.

## Operational Considerations & Next Ideas

- The seeding logic runs only when no movies exist; truncate tables to regenerate the canonical dataset.
- Booking confirmation currently relies on flash messaging—consider adding inline toasts or email hooks for production.
- Posters are served from external URLs; caching or local mirroring may be desirable for reliability.
- For multi-day scheduling, extend the generator to add additional dates while preserving the odd/even cadence.

This document should serve as the source of truth for new contributors ramping onto Tiketa and as a baseline for future architectural decisions.
