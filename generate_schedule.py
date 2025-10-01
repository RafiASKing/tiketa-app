#!/usr/bin/env python3
"""Utility script to maintain a rolling three-day schedule of showtimes."""

from __future__ import annotations
from datetime import datetime, timedelta, time
import pytz

from app import create_app
from app.models import db, Movie, Showtime

# --- PERUBAHAN: Jadikan semua sadar zona waktu ---
JAKARTA_TZ = pytz.timezone('Asia/Jakarta')
UTC = pytz.UTC
START_HOUR = 6  # Jam 6 pagi WIB

EVEN_INTERVAL_HOURS = 3
ODD_INTERVAL_HOURS = 4
EVEN_SLOTS = 6
ODD_SLOTS = 5

def _now_utc_naive() -> datetime:
    return datetime.utcnow().replace(tzinfo=None)


def purge_past_showtimes() -> int:
    """Archive showtimes that have already passed based on the current time."""
    now_utc = _now_utc_naive()

    updated_count = Showtime.query.filter(
        Showtime.time < now_utc,
        Showtime.is_archived.is_(False)
    ).update({Showtime.is_archived: True}, synchronize_session=False)
    
    if updated_count:
        db.session.commit()
    return updated_count or 0

def _generate_slots(studio_number: int) -> tuple[int, int]:
    is_even = studio_number % 2 == 0
    slots = EVEN_SLOTS if is_even else ODD_SLOTS
    interval = EVEN_INTERVAL_HOURS if is_even else ODD_INTERVAL_HOURS
    return slots, interval

def _to_local_naive(utc_dt: datetime) -> datetime:
    """Convert a naive UTC datetime into a naive Jakarta-local datetime."""
    utc_aware = UTC.localize(utc_dt) if utc_dt.tzinfo is None else utc_dt.astimezone(UTC)
    return utc_aware.astimezone(JAKARTA_TZ).replace(tzinfo=None)


def _to_utc_naive(local_dt: datetime) -> datetime:
    """Convert a naive Jakarta-local datetime into a naive UTC datetime."""
    local_aware = JAKARTA_TZ.localize(local_dt) if local_dt.tzinfo is None else local_dt
    return local_aware.astimezone(UTC).replace(tzinfo=None)


def generate_upcoming_showtimes(days: int = 3) -> int:
    """Ensure each movie has scheduled showtimes for the next `days` days."""
    now_local = datetime.now(JAKARTA_TZ).replace(tzinfo=None)
    new_records = 0

    for movie in Movie.query.order_by(Movie.studio_number):
        slots, interval_hours = _generate_slots(movie.studio_number)

        for i in range(days):
            target_date = (now_local + timedelta(days=i)).date()
            day_start_local = datetime.combine(target_date, time.min)
            day_end_local = datetime.combine(target_date, time.max)
            day_start_utc = _to_utc_naive(day_start_local)
            day_end_utc = _to_utc_naive(day_end_local)

            existing_showtimes = (
                Showtime.query
                .filter(
                    Showtime.movie_id == movie.id,
                    Showtime.time.between(day_start_utc, day_end_utc),
                    Showtime.is_archived.is_(False)
                )
                .order_by(Showtime.time)
                .all()
            )

            normalized_existing = {_to_local_naive(st.time) for st in existing_showtimes}

            start_time_local = datetime.combine(target_date, time(hour=START_HOUR))
            expected_times_local = [
                start_time_local + timedelta(hours=interval_hours * slot_index)
                for slot_index in range(slots)
            ]
            expected_normalized = {_to_local_naive(_to_utc_naive(ts)) for ts in expected_times_local}

            # Archive any showtimes that don't align with the expected cadence
            for st in existing_showtimes:
                normalized = _to_local_naive(st.time)
                if normalized not in expected_normalized:
                    st.is_archived = True

            for show_time_local in expected_times_local:
                normalized_show_time = show_time_local.replace(minute=0, second=0, microsecond=0)
                if normalized_show_time in normalized_existing:
                    continue

                show_time_utc = _to_utc_naive(show_time_local)
                db.session.add(Showtime(movie_id=movie.id, time=show_time_utc))
                normalized_existing.add(normalized_show_time)
                new_records += 1

    if new_records:
        db.session.commit()

    return new_records

def main() -> None:
    app = create_app()
    with app.app_context():
        purged = purge_past_showtimes() 
        print(f"Archived {purged} past showtimes.")
        
        created = generate_upcoming_showtimes()
        print(f"Created {created} new upcoming showtimes.")

if __name__ == "__main__":
    main()