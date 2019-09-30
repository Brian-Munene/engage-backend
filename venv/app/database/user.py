from routes import db
from flask import Flask
from flask_bcrypt import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password, 10)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    user_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    name = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(70), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    company_code = db.Column(db.String(70), nullable=True)

    def __init__(self, public_id, name, email, company_code):
        self.name = name
        self.public_id = public_id
        self.email = email
        self.company_code = company_code
