import os
from datetime import datetime, timedelta, time

import pytz
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def seed_initial_data():
    """Seeds the database with genres, movies, and initial showtimes."""
    from app.models import db, Movie, Showtime, Genre
    from app.sample_data.movies import SAMPLE_MOVIES

    if Movie.query.count() != 0:
        print("Database already contains data. Seeding skipped.")
        return

    print("Database is empty, seeding initial data...")

    GENRE_MAP: dict[int, str] = {
        12: "Adventure",
        14: "Fantasy",
        16: "Animation",
        18: "Drama",
        28: "Action",
        35: "Comedy",
        53: "Thriller",
        80: "Crime",
        878: "Science Fiction",
        9648: "Mystery",
        99: "Documentary",
        10749: "Romance",
        10751: "Family",
        10752: "War",
    }

    for genre_id, genre_name in GENRE_MAP.items():
        if not Genre.query.filter_by(id=genre_id).first():
            db.session.add(Genre(id=genre_id, name=genre_name))
    db.session.flush()

    def first_show_datetime() -> datetime:
        jakarta_tz = pytz.timezone('Asia/Jakarta')
        now = datetime.now(jakarta_tz)

        candidate_naive = datetime.combine(now.date(), time(hour=6))
        candidate = jakarta_tz.localize(candidate_naive)

        if candidate <= now:
            candidate_naive = datetime.combine(now.date() + timedelta(days=1), time(hour=6))
            candidate = jakarta_tz.localize(candidate_naive)
        return candidate

    def generate_showtimes(studio_number: int) -> list[datetime]:
        start = first_show_datetime()
        slots = 6 if studio_number % 2 == 0 else 5
        interval_hours = 3 if studio_number % 2 == 0 else 4
        return [start + timedelta(hours=interval_hours * i) for i in range(slots)]

    for movie_data in SAMPLE_MOVIES:
        genre_ids = movie_data.get("genre_ids", [])
        movie_payload = {
            key: value
            for key, value in movie_data.items()
            if key != "genre_ids"
        }

        movie = Movie(**movie_payload)
        db.session.add(movie)
        db.session.flush()

        if genre_ids:
            genres = Genre.query.filter(Genre.id.in_(genre_ids)).all()
            movie.genres.extend(genres)

        for start_time in generate_showtimes(movie.studio_number):
            db.session.add(Showtime(movie_id=movie.id, time=start_time))

    db.session.commit()
    print("Seeding complete.")

# --- FUNGSI CREATE_APP TETAP SAMA ---
def create_app(config=None):
    """Application factory pattern for Flask app creation"""
    app = Flask(__name__, template_folder='../templates')
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///tiketa.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    from app.models import db
    db.init_app(app)
    
    # Register blueprints
    from app.movies import bp as movies_bp
    app.register_blueprint(movies_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
        
    return app