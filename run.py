import os
import click
from app import create_app, seed_initial_data
from app.models import db
from generate_schedule import generate_upcoming_showtimes

# Buat instance aplikasi dari factory
app = create_app()

# Perintah ini sudah ada sebelumnya, untuk membuat tabel kosong
@app.cli.command("reset-db")
def reset_db_command():
    """Drops and recreates all database tables."""
    db.drop_all()
    db.create_all()
    print("Database berhasil di-reset.")

# Perintah ini sudah ada sebelumnya, untuk mengisi data film
@app.cli.command("seed-db")
def seed_db_command():
    """Seeds the database with initial movies and genres."""
    seed_initial_data()

# --- PERINTAH BARU YANG MENGGABUNGKAN SEMUANYA ---
@app.cli.command("full-reset")
def full_reset_command():
    """Drops all tables, recreates them, seeds movies, and generates a 3-day schedule."""
    if click.confirm("PERINGATAN: Ini akan menghapus SEMUA data. Lanjutkan?"):
        print("-> Menghapus semua tabel...")
        db.drop_all()
        print("-> Membuat ulang semua tabel...")
        db.create_all()
        print("-> Mengisi data film & genre awal...")
        seed_initial_data()
        print("-> Membuat jadwal baru untuk 3 hari ke depan...")
        # Panggil fungsi dari skrip yang sudah benar
        generate_upcoming_showtimes() 
        print("\n✅ Reset total dan seeding berhasil diselesaikan.")
    else:
        print("Dibatalkan.")

if __name__ == '__main__':
    # ... (sisa kode run.py Anda untuk menjalankan server development) ...
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true', host='0.0.0.0', port=port)