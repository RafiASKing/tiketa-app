import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
        
        # Initialize with sample data if no movies exist
        from app.models import Movie, Showtime
        from app.sample_data.movies import SAMPLE_MOVIES
        from datetime import datetime, timedelta
        
        if Movie.query.count() == 0:
            # Add sample movies
            for movie_data in SAMPLE_MOVIES:
                movie = Movie(**movie_data)
                db.session.add(movie)
                db.session.flush()  # Get the ID
                
                # Add sample showtimes
                base_time = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
                for i in range(3):  # 3 showtimes per movie
                    showtime = Showtime(
                        movie_id=movie.id,
                        time=base_time + timedelta(days=i)
                    )
                    db.session.add(showtime)
            
            db.session.commit()
    
    return app