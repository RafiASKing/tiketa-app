import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- MULAI BAGIAN BARU ---
def seed_initial_data():
    """Seeds the database with initial movies and genres if it's empty."""
    from app.models import db, Movie, Showtime, Genre
    from app.sample_data.movies import SAMPLE_MOVIES
    from datetime import datetime, timedelta, time

    if Movie.query.count() == 0:
        print("Database is empty, seeding initial data...")
        
        def first_show_datetime() -> datetime:
            now = datetime.now()
            candidate = datetime.combine(now.date(), time(hour=6))
            if candidate <= now:
                candidate = datetime.combine(now.date() + timedelta(days=1), time(hour=6))
            return candidate

        def generate_showtimes(studio_number: int) -> list[datetime]:
            start = first_show_datetime()
            slots = 6 if studio_number % 2 == 0 else 5
            interval_hours = 3 if studio_number % 2 == 0 else 4
            return [start + timedelta(hours=interval_hours * i) for i in range(slots)]

        for movie_data in SAMPLE_MOVIES:
            genre_names = movie_data.get("genres", [])
            movie_payload = {
                key: value
                for key, value in movie_data.items()
                if key not in {"genres", "genre_ids"}
            }

            movie = Movie(**movie_payload)
            db.session.add(movie)
            db.session.flush()

            for genre_name in genre_names:
                genre = Genre.query.filter_by(name=genre_name).first()
                if not genre:
                    genre = Genre(name=genre_name)
                    db.session.add(genre)
                    db.session.flush()
                movie.genres.append(genre)

            for start_time in generate_showtimes(movie.studio_number):
                db.session.add(Showtime(movie_id=movie.id, time=start_time))

        db.session.commit()
        print("Seeding complete.")
    else:
        print("Database already contains data. Seeding skipped.")
# --- AKHIR BAGIAN BARU ---


def create_app(config=None):
    """Application factory pattern for Flask app creation"""
    app = Flask(__name__, template_folder='../templates')
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///tiketa.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Override config if provided
    if config:
        app.config.update(config)
    
    # Initialize extensions
    from app.models import db
    db.init_app(app)
    
    # Register blueprints
    from app.movies import bp as movies_bp
    app.register_blueprint(movies_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
        
        # <<< BLOK SEEDING SUDAH DIHAPUS DARI SINI >>>
    
    return app