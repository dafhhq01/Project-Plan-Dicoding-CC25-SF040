# create_db.py

from app import app
from models import db

with app.app_context():
    db.create_all()
    print("Database berhasil dibuat!")
