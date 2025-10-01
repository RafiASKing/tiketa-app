import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import pytz

# Load environment variables
load_dotenv()

# --- MULAI BAGIAN BARU ---
def seed_initial_data():
    """Seeds the database with initial movies and genres if it's empty."""
    from app.models import db, Movie, Genre
    from app.sample_data.movies import SAMPLE_MOVIES

    if Movie.query.count() == 0:
        print("Database is empty, seeding movies and genres...")
        
        for movie_data in SAMPLE_MOVIES:
            genre_names = movie_data.get("genres", [])
            movie_payload = {
                key: value for key, value in movie_data.items() if key != "genres"
            }

            movie = Movie(**movie_payload)
            db.session.add(movie)
            db.session.flush()

            for genre_name in genre_names:
                genre = Genre.query.filter_by(name=genre_name).first()
                if not genre:
                    genre = Genre(name=genre_name)
                    db.session.add(genre)
                movie.genres.append(genre)

        db.session.commit()
        print("Movie and genre seeding complete.")
    else:
        print("Database already contains movies. Seeding skipped.")


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