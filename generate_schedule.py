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

def purge_past_showtimes() -> int:
    """Archive showtimes that have already passed based on the current time."""
    now_wib = datetime.now(JAKARTA_TZ)
    
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

def generate_upcoming_showtimes(days: int = 3) -> int:
    """Ensure each movie has scheduled showtimes for the next `days` days."""
    now_wib = datetime.now(JAKARTA_TZ)
    new_records = 0

    for i in range(days):
        target_date = (now_wib + timedelta(days=i)).date()
        
        day_start = JAKARTA_TZ.localize(datetime.combine(target_date, time.min))
        day_end = JAKARTA_TZ.localize(datetime.combine(target_date, time.max))

        has_any_schedule = Showtime.query.filter(
            Showtime.time.between(day_start, day_end)
        ).first()

        if has_any_schedule:
            continue

        print(f"Generating schedule for {target_date.strftime('%Y-%m-%d')}...")
        for movie in Movie.query.order_by(Movie.studio_number):
            slots, interval_hours = _generate_slots(movie.studio_number)
            start_time = JAKARTA_TZ.localize(datetime.combine(target_date, time(hour=START_HOUR)))
            
            for slot_index in range(slots):
                show_time = start_time + timedelta(hours=interval_hours * slot_index)
                db.session.add(Showtime(movie_id=movie.id, time=show_time))
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