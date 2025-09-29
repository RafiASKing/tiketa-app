from collections import defaultdict, OrderedDict
from datetime import datetime, date, time, timedelta

from flask import render_template, request, flash, redirect, url_for
from app.movies import bp
from app.models import db, Movie, Showtime, Booking
from app.layouts import SEAT_MAP

@bp.route('/')
def index():
    """Main route to list all movies, ordered by studio."""
    movies = Movie.query.order_by(Movie.studio_number).all()
    return render_template('movies/index.html', movies=movies)

@bp.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    """Show movie details and showtimes"""
    movie = Movie.query.get_or_404(movie_id)
    now = datetime.now()
    end_date = date.today() + timedelta(days=2)
    horizon = datetime.combine(end_date, time.max)

    upcoming_showtimes = (
        Showtime.query
        .filter(
            Showtime.movie_id == movie_id,
            Showtime.time >= now,
            Showtime.time <= horizon,
            Showtime.is_archived.is_(False)
        )
        .order_by(Showtime.time)
        .all()
    )

    grouped = defaultdict(list)
    for showtime in upcoming_showtimes:
        grouped[showtime.time.date()].append(showtime)

    grouped_showtimes = OrderedDict(
        sorted(grouped.items(), key=lambda item: item[0])
    )

    return render_template(
        'movies/detail.html',
        movie=movie,
        grouped_showtimes=grouped_showtimes,
        timedelta=timedelta
    )

@bp.route('/book/<int:showtime_id>', methods=['GET', 'POST'])
def book_ticket(showtime_id):
    """Book a ticket for a showtime"""
    showtime = Showtime.query.get_or_404(showtime_id)
    
    if request.method == 'POST':
        user = request.form.get('user')
        seat = request.form.get('seat')
        
        if user and seat:
            # Check if seat is already booked
            existing_booking = Booking.query.filter_by(
                showtime_id=showtime_id, 
                seat=seat
            ).first()
            
            if existing_booking:
                flash(f'Seat {seat} is already booked!', 'error')
            else:
                booking = Booking(
                    user=user,
                    seat=seat,
                    showtime_id=showtime_id
                )
                db.session.add(booking)
                db.session.commit()
                flash(f'Berhasil booking seat {seat} untuk {user}!', 'success')
                return redirect(url_for('movies.book_ticket', showtime_id=showtime_id))
        else:
            flash('Silakan provide nama pemesan dan no seat.', 'error')

    # Gather booking details for the seating chart
    bookings = (
        Booking.query
        .filter_by(showtime_id=showtime_id)
        .order_by(Booking.seat)
        .all()
    )
    booked_seats = {
        booking.seat: {
            "user": booking.user,
            "booked_at": booking.created_at
        }
        for booking in bookings
    }

    return render_template(
        'movies/book.html',
        showtime=showtime,
        booked_seats=booked_seats,
        seat_map=SEAT_MAP,
        timedelta=timedelta
    )