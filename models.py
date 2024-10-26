from db import db
from flask_login import UserMixin

# Define a simple User model for demonstration
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to the User table
    supplier = db.relationship('User', backref=db.backref('parts', lazy=True))
    price = db.Column(db.Float, nullable=False)
    availability = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    delivery = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=False)

