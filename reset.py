import os
from dotenv import load_dotenv

# Pastikan environment variables dari .env dimuat
load_dotenv()

from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    print("Menghapus semua tabel dari database...")
    db.drop_all()
    print("Membuat ulang semua tabel...")
    db.create_all()
    print("Database berhasil di-reset!")
