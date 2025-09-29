from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

movie_genres = db.Table(
    'movie_genres',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)


class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    studio_number = db.Column(db.Integer, unique=True, nullable=False)
    poster_path = db.Column(db.String(255), nullable=True)
    backdrop_path = db.Column(db.String(255), nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    trailer_youtube_id = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with showtimes
    showtimes = db.relationship(
        'Showtime',
        backref='movie',
        lazy=True,
        order_by='Showtime.time'
    )

    genres = db.relationship(
        'Genre',
        secondary=movie_genres,
        back_populates='movies',
        lazy='joined'
    )
    
    def __repr__(self):
        return f'<Movie {self.title}>'


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    movies = db.relationship(
        'Movie',
        secondary=movie_genres,
        back_populates='genres'
    )

    def __repr__(self):
        return f'<Genre {self.name}>'

class Showtime(db.Model):
    __tablename__ = 'showtimes'
    
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with bookings
    bookings = db.relationship('Booking', backref='showtime', lazy=True)
    
    def __repr__(self):
        return f'<Showtime {self.movie.title} at {self.time}>'

class Booking(db.Model):
    __tablename__ = 'bookings'

    __table_args__ = (
        db.UniqueConstraint('showtime_id', 'seat', name='uq_booking_showtime_seat'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255), nullable=False)
    seat = db.Column(db.String(10), nullable=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtimes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Booking {self.user} - Seat {self.seat}>'