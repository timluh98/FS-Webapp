from db import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    supplier = db.relationship('User', backref=db.backref('parts', lazy=True, cascade="all, delete-orphan"))
    price = db.Column(db.Float, nullable=False)
    availability = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    delivery = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)  
    model = db.Column(db.String(100), nullable=False)
    purchases = db.relationship('Purchase', back_populates='part', lazy=True)

    def update_availability(self):
        self.availability = 'Out of Stock' if self.quantity <= 0 else 'In Stock'

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('part.id'), nullable=False)
    part = db.relationship('Part', back_populates='purchases', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('purchases', lazy=True))
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    card_number = db.Column(db.String(20), nullable=False)
    cvc = db.Column(db.String(4), nullable=False)
    exp_date = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)