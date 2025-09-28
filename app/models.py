from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with showtimes
    showtimes = db.relationship('Showtime', backref='movie', lazy=True)
    
    def __repr__(self):
        return f'<Movie {self.title}>'

class Showtime(db.Model):
    __tablename__ = 'showtimes'
    
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with bookings
    bookings = db.relationship('Booking', backref='showtime', lazy=True)
    
    def __repr__(self):
        return f'<Showtime {self.movie.title} at {self.time}>'

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255), nullable=False)
    seat = db.Column(db.String(10), nullable=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtimes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Booking {self.user} - Seat {self.seat}>'