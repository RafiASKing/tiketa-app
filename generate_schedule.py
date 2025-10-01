#!/usr/bin/env python3
"""Utility script to maintain a rolling three-day schedule of showtimes."""

from __future__ import annotations
from datetime import datetime, timedelta, time
import pytz

from app import create_app
from app.models import db, Movie, Showtime

# --- PERUBAHAN: Jadikan semua sadar zona waktu ---
JAKARTA_TZ = pytz.timezone('Asia/Jakarta')
START_HOUR = 6  # Jam 6 pagi WIB

EVEN_INTERVAL_HOURS = 3
ODD_INTERVAL_HOURS = 4
EVEN_SLOTS = 6
ODD_SLOTS = 5

def _now_local_naive() -> datetime:
    return datetime.now(JAKARTA_TZ).replace(tzinfo=None)


def purge_past_showtimes() -> int:
    """Archive showtimes that have already passed based on the current time."""
    now_wib = _now_local_naive()
    
    # Hanya arsipkan yang sudah lewat dari jam sekarang
    updated_count = Showtime.query.filter(
        Showtime.time < now_wib,
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

def _normalize_to_local(dt: datetime) -> datetime:
    """Convert any datetime to Jakarta-local naive time rounded to the hour."""
    if dt.tzinfo is not None:
        dt = dt.astimezone(JAKARTA_TZ).replace(tzinfo=None)
    return dt.replace(minute=0, second=0, microsecond=0)


def generate_upcoming_showtimes(days: int = 3) -> int:
    """Ensure each movie has scheduled showtimes for the next `days` days."""
    now_wib = _now_local_naive()
    new_records = 0

    for movie in Movie.query.order_by(Movie.studio_number):
        slots, interval_hours = _generate_slots(movie.studio_number)

        for i in range(days):
            target_date = (now_wib + timedelta(days=i)).date()
            day_start = datetime.combine(target_date, time.min)
            day_end = datetime.combine(target_date, time.max)

            existing_showtimes = (
                Showtime.query
                .filter(
                    Showtime.movie_id == movie.id,
                    Showtime.time.between(day_start, day_end),
                    Showtime.is_archived.is_(False)
                )
                .order_by(Showtime.time)
                .all()
            )

            normalized_existing = {_normalize_to_local(st.time) for st in existing_showtimes}

            start_time = datetime.combine(target_date, time(hour=START_HOUR))
            expected_times = [
                start_time + timedelta(hours=interval_hours * slot_index)
                for slot_index in range(slots)
            ]
            expected_normalized = {_normalize_to_local(ts) for ts in expected_times}

            # Archive any showtimes that don't align with the expected cadence
            for st in existing_showtimes:
                normalized = _normalize_to_local(st.time)
                if normalized not in expected_normalized:
                    st.is_archived = True

            for show_time in expected_times:
                normalized_show_time = _normalize_to_local(show_time)
                if normalized_show_time in normalized_existing:
                    continue

                db.session.add(Showtime(movie_id=movie.id, time=normalized_show_time))
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