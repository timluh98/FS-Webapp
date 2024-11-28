import os
import json
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import User, Part, Purchase
from forms import RegistrationForm, LoginForm, OfferPartForm, PurchaseForm, ProfileForm

# App Configuration
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.update(
    SECRET_KEY='secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME='pulse',
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(basedir, "instance", "automotive_parts.sqlite")}',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# Initialize extensions
db.init_app(app)
Bootstrap5(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def init_db():
    with app.app_context():
        db.create_all()

def load_json_data(filename='parts.json'):
    with open(os.path.join(basedir, filename), 'r') as f:
        return json.load(f)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('catalogue_index.html', parts=load_json_data('static/data/parts.json'))

@app.route('/catalogue')
def catalogue():
    query = Part.query
    search = request.args.get('search', '')
    manufacturer = request.args.get('manufacturer', '')
    price_order = request.args.get('price_order', '')

    if search:
        query = query.filter(Part.name.ilike(f'%{search}%'))
    if manufacturer:
        query = query.filter_by(manufacturer=manufacturer)
    if price_order:
        query = query.order_by(Part.price.asc() if price_order == 'asc' else Part.price.desc())

    return render_template('catalogue.html', 
                         parts=query.all(),
                         manufacturers=Part.query.with_entities(Part.manufacturer).distinct().all())

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if not form.validate_on_submit():
        return render_template('register.html', form=form)

    if User.query.filter_by(email=form.email.data).first():
        flash('Email already registered. Please log in.', 'danger')
        return redirect(url_for('login'))

    if User.query.filter_by(username=form.username.data).first():
        flash('Username already taken. Please choose a different username.', 'danger')
        return redirect(url_for('register'))

    db.session.add(User(
        username=form.username.data,
        email=form.email.data,
        password=generate_password_hash(form.password.data),
        role=form.role.data
    ))
    db.session.commit()
    flash('Registration successful! Please log in.', 'success')
    return redirect(url_for('login'))

@app.route('/part/<int:part_id>', methods=['GET', 'POST'])
def view_part(part_id):
    part = Part.query.get_or_404(part_id)
    form = PurchaseForm()
    
    if not form.validate_on_submit():
        return render_template('view_part.html', part=part, form=form)

    if part.quantity <= 0:
        flash('This item is out of stock!', 'error')
        return redirect(url_for('view_part', part_id=part.id))

    if form.quantity.data > part.quantity:
        flash('Not enough items in stock!', 'error')
        return redirect(url_for('view_part', part_id=part.id))

    purchase = Purchase(
        part_id=part.id,
        user_id=current_user.id,
        name=form.name.data,
        address=form.address.data,
        card_number=form.card_number.data,
        cvc=form.cvc.data,
        exp_date=datetime(int(form.exp_year.data), int(form.exp_month.data), 1),
        quantity=form.quantity.data,
        total_price=part.price * form.quantity.data
    )

    db.session.add(purchase)
    part.quantity -= form.quantity.data
    part.update_availability()
    db.session.commit()
    
    flash('Purchase successful!', 'success')
    return redirect(url_for('catalogue'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

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
            ext = form.image.data.filename.rsplit('.', 1)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
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
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error saving part: {str(e)}', 'danger')
        return render_template('offer_part.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if not check_password_hash(current_user.password, form.current_password.data):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('profile'))

        if form.new_password.data and check_password_hash(current_user.password, form.new_password.data):
            flash('New password must be different from your current password.', 'danger')
            return redirect(url_for('profile'))

        if form.email.data != current_user.email:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user and existing_user.id != current_user.id:
                flash('This email address is already in use.', 'danger')
                return redirect(url_for('profile'))

        try:
            if form.email.data != current_user.email:
                current_user.email = form.email.data
            if form.new_password.data:
                current_user.password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('index'))
        except SQLAlchemyError:
            db.session.rollback()
            flash('An error occurred while updating your profile. Please try again.', 'danger')
            return redirect(url_for('profile'))

    form.email.data = current_user.email
    return render_template('profile.html', form=form)

@app.route('/delete-part/<int:part_id>', methods=['POST'])
@login_required
def delete_part(part_id):
    part = Part.query.get_or_404(part_id)
    if part.supplier_id != current_user.id:
        flash('You do not have permission to delete this part.', 'danger')
        return redirect(url_for('catalogue'))

    try:
        db.session.delete(part)
        db.session.commit()
        flash('Part deleted successfully!', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'An error occurred while deleting the part: {str(e)}', 'danger')
    return redirect(url_for('catalogue'))

@app.route('/my_orders')
@login_required
def my_orders():
    return render_template('my_orders.html', 
                         purchases=Purchase.query.filter_by(user_id=current_user.id).all())

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)