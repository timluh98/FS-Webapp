import os
import json
import logging
from datetime import datetime

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort,
)
from flask_bootstrap import Bootstrap5
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import User, Part, Purchase
from forms import (
    RegistrationForm,
    LoginForm,
    OfferPartForm,
    PurchaseForm,
    ProfileForm,
)

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# App Configuration
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config.update(
    SECRET_KEY='secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME='pulse',
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(basedir, "instance", "automotive_parts.sqlite")}',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Initialize Extensions
db.init_app(app)
Bootstrap5(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Database Initialization
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        logger.info("Database initialized.")


# User Loader Callback
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.query.get(int(user_id))


# Helper Functions
def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_json_data(filename='parts.json'):
    """Load JSON data from a file."""
    try:
        with open(os.path.join(basedir, filename), 'r') as f:
            data = json.load(f)
            logger.info(f"Loaded data from {filename}.")
            return data
    except FileNotFoundError:
        logger.error(f"{filename} not found.")
        return {}


# Routes
@app.route('/')
def index():
    """Render the homepage with parts from the JSON file."""
    parts = load_json_data('static/data/parts.json')
    return render_template('catalogue_index.html', parts=parts)


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
    """Handle user registration."""
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if email or username already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered. Please log in.', 'danger')
            logger.warning(f"Registration attempt with existing email: {form.email.data}")
            return redirect(url_for('login'))

        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken. Please choose a different username.', 'danger')
            logger.warning(f"Registration attempt with existing username: {form.username.data}")
            return redirect(url_for('register'))

        # Create new user
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            role=form.role.data
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            logger.info(f"New user registered: {new_user.username}")
            return redirect(url_for('login'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            logger.error(f"Error during registration: {e}")
            return redirect(url_for('register'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            logger.info(f"User logged in: {user.username}")
            return redirect(url_for('index'))
        flash('Invalid email or password.', 'danger')
        logger.warning(f"Failed login attempt for email: {form.email.data}")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash('You have been logged out.', 'info')
    logger.info(f"User logged out.")
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Allow users to update their profile information."""
    form = ProfileForm()
    if form.validate_on_submit():
        # Verify current password
        if not check_password_hash(current_user.password, form.current_password.data):
            flash('Current password is incorrect.', 'danger')
            logger.warning(f"Incorrect password attempt by user: {current_user.username}")
            return redirect(url_for('profile'))

        # Check if new password is different
        if form.new_password.data and check_password_hash(current_user.password, form.new_password.data):
            flash('New password must be different from your current password.', 'danger')
            logger.warning(f"User {current_user.username} attempted to set the same password.")
            return redirect(url_for('profile'))

        # Check if email is changing and if it's unique
        if form.email.data != current_user.email:
            if User.query.filter_by(email=form.email.data).first():
                flash('This email address is already in use.', 'danger')
                logger.warning(f"User {current_user.username} attempted to change to an existing email: {form.email.data}")
                return redirect(url_for('profile'))
            current_user.email = form.email.data
            logger.info(f"User {current_user.username} changed email to: {form.email.data}")

        # Update password if provided
        if form.new_password.data:
            current_user.password = generate_password_hash(form.new_password.data)
            logger.info(f"User {current_user.username} updated their password.")

        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            logger.info(f"User {current_user.username} updated their profile.")
            return redirect(url_for('index'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('An error occurred while updating your profile. Please try again.', 'danger')
            logger.error(f"Error updating profile for user {current_user.username}: {e}")
            return redirect(url_for('profile'))

    # Pre-fill form with current email
    form.email.data = current_user.email
    return render_template('profile.html', form=form)


@app.route('/part/<int:part_id>', methods=['GET', 'POST'])
@login_required
def view_part(part_id):
    """View details of a specific part and handle purchases."""
    part = Part.query.get_or_404(part_id)
    form = PurchaseForm()

    if form.validate_on_submit():
        if part.quantity <= 0:
            flash('This item is out of stock!', 'danger')
            logger.info(f"Out of stock purchase attempt for part ID: {part_id} by user: {current_user.username}")
            return redirect(url_for('view_part', part_id=part.id))

        if form.quantity.data > part.quantity:
            flash('Not enough items in stock!', 'danger')
            logger.info(f"Insufficient stock purchase attempt for part ID: {part_id} by user: {current_user.username}")
            return redirect(url_for('view_part', part_id=part.id))

        # Create Purchase
        purchase = Purchase(
            part_id=part.id,
            user_id=current_user.id,
            name=form.name.data,
            address=form.address.data,
            card_number=form.card_number.data,  # TODO: Storing raw card details is insecure
            cvc=form.cvc.data,                  
            exp_date=datetime(int(form.exp_year.data), int(form.exp_month.data), 1),
            quantity=form.quantity.data,
            total_price=part.price * form.quantity.data
        )

        try:
            db.session.add(purchase)
            part.quantity -= form.quantity.data
            part.update_availability()  
            db.session.commit()
            flash('Purchase successful!', 'success')
            logger.info(f"User {current_user.username} purchased part ID: {part_id}, Quantity: {form.quantity.data}")
            return redirect(url_for('catalogue'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('An error occurred during the purchase. Please try again.', 'danger')
            logger.error(f"Error during purchase by user {current_user.username}: {e}")
            return redirect(url_for('view_part', part_id=part.id))

    return render_template('view_part.html', part=part, form=form)


@app.route('/offer-part', methods=['GET', 'POST'])
@login_required
def offer_part():
    """Allow suppliers to offer new parts."""
    if current_user.role != 'supplier':
        flash('Only suppliers can offer parts.', 'danger')
        logger.warning(f"User {current_user.username} with role {current_user.role} attempted to offer a part.")
        return redirect(url_for('index'))

    form = OfferPartForm()
    if form.validate_on_submit():
        image_filename = None
        if form.image.data and allowed_file(form.image.data.filename):
            image_filename = secure_filename(form.image.data.filename)
            image_path = os.path.join(app.root_path, "static/images", image_filename)
            form.image.data.save(image_path)
            logger.info(f"Image saved: {image_filename}")

        # Create new Part
        new_part = Part(
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
        )

        try:
            db.session.add(new_part)
            db.session.commit()
            flash('Part offer submitted successfully!', 'success')
            logger.info(f"User {current_user.username} offered new part: {new_part.name}")
            return redirect(url_for('index'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('An error occurred while offering the part. Please try again.', 'danger')
            logger.error(f"Error offering part by user {current_user.username}: {e}")
            return render_template('offer_part.html', form=form)

    return render_template('offer_part.html', form=form)

@app.route('/my_listings')
@login_required
def my_listings():
    """Display the supplier's listings."""
    if current_user.role != 'supplier':
        flash('Only suppliers can view their listings.', 'danger')
        return redirect(url_for('index'))

    parts = Part.query.filter_by(supplier_id=current_user.id).all()
    return render_template('my_listings.html', parts=parts)

@app.route('/edit-part/<int:part_id>', methods=['GET', 'POST'])
@login_required
def edit_part(part_id):
    """Edit details of a specific part."""
    part = Part.query.get_or_404(part_id)
    if part.supplier_id != current_user.id:
        flash('You do not have permission to edit this part.', 'danger')
        logger.warning(f"User {current_user.username} attempted to edit part ID: {part_id} they do not own.")
        return redirect(url_for('catalogue'))
    
    form = OfferPartForm(obj=part)
    
    if form.validate_on_submit():
        try:
            # Explicitly handle quantity assignment
            quantity = form.quantity.data
            if quantity is not None:  # Make sure we have a value
                part.quantity = quantity
                part.name = form.name.data
                part.manufacturer = form.manufacturer.data
                part.model = form.model.data
                part.price = form.price.data
                part.delivery = form.delivery.data
                part.description = form.description.data
                
                # Handle image if provided
                if form.image.data and allowed_file(form.image.data.filename):
                    image_filename = secure_filename(form.image.data.filename)
                    image_path = os.path.join(app.root_path, "static/images", image_filename)
                    form.image.data.save(image_path)
                    part.image = image_filename
                    logger.info(f"Image updated: {image_filename}")
                
                # Update availability after quantity change
                part.update_availability()
                
                db.session.commit()
                flash('Part updated successfully!', 'success')
                logger.info(f"User {current_user.username} updated part ID: {part_id} - Quantity set to {quantity}")
                return redirect(url_for('my_listings'))
            else:
                flash('Invalid quantity value', 'danger')
                
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('An error occurred while updating the part. Please try again.', 'danger')
            logger.error(f"Error updating part ID: {part_id} by user {current_user.username}: {e}")
            
    return render_template('edit_part.html', form=form, part=part)


@app.route('/delete-part/<int:part_id>', methods=['POST'])
@login_required
def delete_part(part_id):
    """Delete a part offered by the supplier."""
    part = Part.query.get_or_404(part_id)
    if part.supplier_id != current_user.id:
        flash('You do not have permission to delete this part.', 'danger')
        logger.warning(f"User {current_user.username} attempted to delete part ID: {part_id} they do not own.")
        abort(403)

    try:
        db.session.delete(part)
        db.session.commit()
        flash('Part deleted successfully!', 'success')
        logger.info(f"User {current_user.username} deleted part ID: {part_id}")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('An error occurred while deleting the part. Please try again.', 'danger')
        logger.error(f"Error deleting part ID: {part_id} by user {current_user.username}: {e}")

    return redirect(url_for('catalogue'))


@app.route('/my_orders')
@login_required
def my_orders():
    """Display the user's purchase history."""
    purchases = Purchase.query.filter_by(user_id=current_user.id).all()
    logger.info(f"User {current_user.username} viewed their orders.")
    return render_template('my_orders.html', purchases=purchases)


@app.route('/faq')
def faq():
    """Display the FAQ page."""
    return render_template('faq.html')


# Main Execution
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
