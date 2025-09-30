#!/usr/bin/env python3
"""
Tiketa Flask Application Entry Point
"""
import os
from app import create_app

app = create_app()

@app.cli.command("reset-db")
def reset_db_command():
    """Menghapus dan membuat ulang semua tabel database."""
    from app.models import db
    with app.app_context():
        db.drop_all()
        db.create_all()
    print("Database berhasil di-reset.")

# --- TAMBAHKAN PERINTAH BARU DI SINI ---
@app.cli.command("seed-db")
def seed_db_command():
    """Memasukkan data awal ke dalam database."""
    from app import seed_initial_data
    with app.app_context():
        seed_initial_data()
# --- AKHIR PERINTAH BARU ---

if __name__ == '__main__':
    # Use environment variables for configuration in production
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    app.run(debug=debug, host='0.0.0.0', port=port)