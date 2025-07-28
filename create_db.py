# create_db.py
from app import app, db
from argon2 import PasswordHasher
from models.user import User

with app.app_context():
    db.create_all()  # Create tables

    # Create admin user
    ph = PasswordHasher()
    admin_password = ph.hash("1234")
    admin_user = User(username="admin", password=admin_password)
    
    db.session.add(admin_user)
    db.session.commit()
