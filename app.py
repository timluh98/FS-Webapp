import os
import json
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from db import db  # Import the db instance
from models import User, Part, Purchase  # Import the User and Part model
from forms import RegistrationForm, LoginForm, OfferPartForm, PurchaseForm  # Import the forms
from datetime import datetime

app = Flask(__name__)

# Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME='pulse',
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(basedir, "instance", "automotive_parts.sqlite")}',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# Initialize the database with the app
db.init_app(app)
Bootstrap5(app)

# Set up login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to the login page if the user is not authenticated

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables if they don't exist
with app.app_context():
    db.create_all()

def load_json_data(filename='parts.json'):
    json_path = os.path.join(basedir, filename)
    with open(json_path, 'r') as json_file:
        return json.load(json_file)


@app.route('/')
def index():
    parts_data = load_json_data('static/data/parts.json')
    return render_template('catalogue_index.html', parts=parts_data)

@app.route('/catalogue')
def catalogue():
    search_query = request.args.get('search', '')
    if search_query:
        parts = Part.query.filter(Part.name.ilike(f'%{search_query}%')).all()
    else:
        parts = Part.query.all()
    return render_template('catalogue.html', parts=parts)

@app.route('/insert/sample')
def run_insert_sample():
    insert_sample()
    return 'Database flushed and populated with some sample data.'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('login'))

        # Create a new user with hashed password and selected role
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password, 
            role=form.role.data  
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/part/<int:part_id>', methods=['GET', 'POST'])
def view_part(part_id):
    part = Part.query.get_or_404(part_id)
    form = PurchaseForm()
    if form.validate_on_submit():

        name = form.name.data
        address = form.address.data
        card_number = form.card_number.data
        cvc = form.cvc.data  
        exp_month = form.exp_month.data
        exp_year = form.exp_year.data

        purchase = Purchase(
            part_id=part.id,
            user_id=current_user.id,
            name=name,
            address=address,
            card_number=card_number,
            cvc=cvc,  
            exp_date=datetime(int(exp_year), int(exp_month), 1) 
        )
        db.session.add(purchase)
        db.session.commit()

        flash('Purchase successful!', 'success')
        return redirect(url_for('index'))
    return render_template('view_part.html', part=part, form=form)

@app.route('/faq')
def faq():
    return render_template('faq.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Check if the user exists and if the password is correct
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))

        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/offer-part', methods=['GET', 'POST'])
@login_required
def offer_part():
    if current_user.role != 'supplier':
        flash('Only suppliers can offer parts.', 'danger')
        return redirect(url_for('index'))

    form = OfferPartForm()
    if not form.validate_on_submit():
        return render_template('offer_part.html', form=form)

    try:
        image_filename = None
        if form.image.data and '.' in form.image.data.filename:
            if form.image.data.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                image_filename = secure_filename(form.image.data.filename)
                form.image.data.save(os.path.join(app.root_path, "static/images", image_filename))

        db.session.add(Part(
            name=form.name.data,
            manufacturer=form.manufacturer.data,
            model=form.model.data,
            price=form.price.data,
            availability=form.availability.data,
            quantity=form.quantity.data,
            delivery=form.delivery.data,
            image=image_filename,
            description=form.description.data,
            supplier_id=current_user.id
        ))
        db.session.commit()
        flash('Part offer submitted successfully!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error saving part: {str(e)}', 'danger')
        return render_template('offer_part.html', form=form)
    
# Sample data insertion function
def insert_sample():
    db.session.execute(db.delete(User))
    user1 = User(username='testuser1', email='test1@example.com', password='password123', role='supplier')
    user2 = User(username='testuser2', email='test2@example.com', password='password123', role='customer')
    db.session.add_all([user1, user2])
    db.session.commit()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)