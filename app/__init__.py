import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- FUNGSI SEEDING YANG SUDAH DIPERBAIKI TOTAL ---
def seed_initial_data():
    """Seeds the database with genres and movies using genre_ids."""
    from app.models import db, Movie, Showtime, Genre
    from app.sample_data.movies import SAMPLE_MOVIES
    
    # Kamus untuk menerjemahkan ID menjadi Nama Genre (seperti dari API TMDb)
    GENRE_MAP = {
        16: "Animation", 12: "Adventure", 10751: "Family",
        18: "Drama", 10749: "Romance", 28: "Action",
        878: "Science Fiction", 53: "Thriller", 80: "Crime",
        35: "Comedy"
    }

    if Movie.query.count() == 0:
        print("Database is empty, seeding initial data...")
        
        # 1. Isi tabel Genre terlebih dahulu
        print("-> Seeding genres...")
        for genre_id, genre_name in GENRE_MAP.items():
            # Cek jika genre sudah ada, jika tidak, buat baru
            existing_genre = Genre.query.filter_by(id=genre_id).first()
            if not existing_genre:
                genre = Genre(id=genre_id, name=genre_name)
                db.session.add(genre)
        db.session.commit()

        # 2. Proses data film
        print("-> Seeding movies and relationships...")
        for movie_data in SAMPLE_MOVIES:
            # Ambil genre_ids dari data
            genre_ids = movie_data.get("genre_ids", [])
            
            # Buat payload untuk Movie, buang field genre
            movie_payload = {
                key: value for key, value in movie_data.items() if key != "genre_ids"
            }

            # Buat objek Movie
            movie = Movie(**movie_payload)
            db.session.add(movie)
            
            # Hubungkan genre berdasarkan ID
            if genre_ids:
                # Ambil objek genre dari DB berdasarkan daftar ID
                genres_to_link = Genre.query.filter(Genre.id.in_(genre_ids)).all()
                movie.genres.extend(genres_to_link)

        db.session.commit()
        print("Seeding complete.")
    else:
        print("Database already contains movies. Seeding skipped.")

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