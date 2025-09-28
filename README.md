# Tiketa - Movie Ticket Booking App

A modular web application for booking movie tickets built with Python, Flask, PostgreSQL, and Flask-SQLAlchemy.

## Features

- **Movie Listings**: Browse available movies with descriptions
- **Showtime Management**: View showtimes for each movie
- **Ticket Booking**: Book tickets with seat selection
- **Database Integration**: PostgreSQL support with SQLite fallback
- **Modular Architecture**: Built using Flask's Application Factory Pattern and Blueprints

## Architecture

The application follows the **Application Factory Pattern** with **Blueprints** for modular structure:

```
tiketa-app/
├── app/
│   ├── __init__.py         # Application factory
│   ├── models.py           # Database models
│   └── movies/             # Movies blueprint
│       ├── __init__.py
│       └── routes.py       # Movie routes
├── templates/
│   └── movies/             # Movie templates
│       ├── index.html      # Movie listings
│       ├── detail.html     # Movie details & showtimes
│       └── book.html       # Ticket booking
├── requirements.txt        # Dependencies
├── run.py                 # Application entry point
└── .env.example          # Environment configuration template
```

## Database Models

- **Movie**: Stores movie information (title, description)
- **Showtime**: Links movies to specific show times
- **Booking**: Records user bookings with seat assignments

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd tiketa-app
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database configuration
   ```

5. **Set up database**:
   - For PostgreSQL: Set `DATABASE_URL=postgresql://username:password@localhost/database_name`
   - For SQLite (default): `DATABASE_URL=sqlite:///tiketa.db`

6. **Run the application**:
   ```bash
   python run.py
   ```

The application will be available at `http://localhost:5000`

## Database Configuration

The application uses the `DATABASE_URL` environment variable for database connection:

- **PostgreSQL**: `postgresql://username:password@host:port/database`
- **SQLite**: `sqlite:///path/to/database.db` (default fallback)

## Routes

- `/` - List all available movies (main route)
- `/movie/<id>` - View movie details and showtimes
- `/book/<showtime_id>` - Book tickets for a specific showtime

## Sample Data

The application automatically creates sample movies and showtimes on first run:
- The Dark Knight
- Inception  
- Pulp Fiction

Each movie has 3 sample showtimes for testing.

## Development

To run in development mode:
```bash
export FLASK_DEBUG=true
python run.py
```

## Technologies Used

- **Python 3.12+**
- **Flask 3.0.0** - Web framework
- **Flask-SQLAlchemy 3.1.1** - Database ORM
- **PostgreSQL** - Primary database
- **SQLite** - Development/fallback database
- **HTML/CSS/JavaScript** - Frontend
- **python-dotenv** - Environment configuration

## License

MIT License - see LICENSE file for details.