#!/usr/bin/env python3
"""Utility script to maintain a rolling three-day schedule of showtimes."""

from __future__ import annotations

from datetime import datetime, timedelta, time

from app import create_app
from app.models import db, Movie, Showtime


START_HOUR = 7  # 07:00 local time for the first show
EVEN_INTERVAL_HOURS = 3
ODD_INTERVAL_HOURS = 4
EVEN_SLOTS = 6
ODD_SLOTS = 5


def purge_past_showtimes(cutoff: datetime | None = None) -> int:
    """Delete showtimes that end before the start of ``cutoff`` (default: today).

    Returns the number of records removed.
    """
    if cutoff is None:
        cutoff = datetime.combine(datetime.now().date(), time())

    deleted = (
        Showtime.query
        .filter(Showtime.time < cutoff)
        .delete(synchronize_session=False)
    )

    if deleted:
        db.session.commit()
    return deleted or 0


def _generate_slots(studio_number: int) -> tuple[int, int]:
    is_even = studio_number % 2 == 0
    slots = EVEN_SLOTS if is_even else ODD_SLOTS
    interval = EVEN_INTERVAL_HOURS if is_even else ODD_INTERVAL_HOURS
    return slots, interval


def generate_upcoming_showtimes(days: int = 3) -> int:
    """Ensure each movie has scheduled showtimes for the next ``days`` days.

    Returns the number of new showtimes inserted.
    """
    today = datetime.now().date()
    window = [today + timedelta(days=i) for i in range(days)]
    new_records = 0

    for movie in Movie.query.order_by(Movie.studio_number):
        slots, interval_hours = _generate_slots(movie.studio_number)

        for show_date in window:
            start_time = datetime.combine(show_date, time(hour=START_HOUR))

            for slot_index in range(slots):
                show_time = start_time + timedelta(hours=interval_hours * slot_index)

                exists = Showtime.query.filter_by(
                    movie_id=movie.id,
                    time=show_time
                ).first()

                if exists:
                    continue

                db.session.add(Showtime(movie_id=movie.id, time=show_time))
                new_records += 1

    if new_records:
        db.session.commit()

    return new_records


def main() -> None:
    app = create_app()
    with app.app_context():
        purged = purge_past_showtimes()
        created = generate_upcoming_showtimes()
        print(f"Purged {purged} past showtimes, created {created} upcoming showtimes.")


if __name__ == "__main__":
    main()
