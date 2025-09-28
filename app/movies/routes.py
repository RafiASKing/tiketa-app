from datetime import timedelta

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
    showtimes = Showtime.query.filter_by(movie_id=movie_id).order_by(Showtime.time).all()
    return render_template('movies/detail.html', movie=movie, showtimes=showtimes, timedelta=timedelta)

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
                flash(f'Successfully booked seat {seat} for {user}!', 'success')
                return redirect(url_for('movies.book_ticket', showtime_id=showtime_id))
        else:
            flash('Please provide both user name and seat number.', 'error')
    
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