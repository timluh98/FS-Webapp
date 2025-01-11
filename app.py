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
    session,
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
from flask_migrate import Migrate

from db import db
from models import User, Part, Purchase, Order
from forms import (
    RegistrationForm,
    LoginForm,
    OfferPartForm,
    CartForm,
    ProfileForm 
)

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# App Configuration
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config.update(
    SECRET_KEY='secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME='flatly',
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(basedir, "instance", "automotive_parts.sqlite")}',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Initialize Extensions
db.init_app(app)
migrate = Migrate(app, db)
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
    supplier_orders_count = 0
    
    if current_user.is_authenticated and current_user.role == 'supplier':
        supplier_orders = (Order.query
            .join(Purchase)
            .join(Part)
            .filter(Part.supplier_id == current_user.id)
            .filter(Order.payment_status == 'paid')
            .filter(Order.shipping_status == 'pending')
            .distinct()
            .count())
        supplier_orders_count = supplier_orders
        
    return render_template('catalogue_index.html', 
                         parts=parts,
                         supplier_orders_count=supplier_orders_count)


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

    supplier_orders_count = 0
    if current_user.is_authenticated and current_user.role == 'supplier':
        supplier_orders = (Order.query
            .join(Purchase)
            .join(Part)
            .filter(Part.supplier_id == current_user.id)
            .filter(Order.payment_status == 'paid')
            .filter(Order.shipping_status == 'pending')
            .distinct()
            .count())
        supplier_orders_count = supplier_orders

    return render_template('catalogue.html', 
                         parts=query.all(),
                         manufacturers=Part.query.with_entities(Part.manufacturer).distinct().all(),
                         supplier_orders_count=supplier_orders_count)


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


@app.route('/part/<int:part_id>', methods=['GET'])
@login_required
def view_part(part_id):
    part = Part.query.get_or_404(part_id)
    return render_template('view_part.html', part=part)


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
            if quantity is not None:  
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

@app.route('/add_to_cart/<int:part_id>', methods=['POST'])
@login_required
def add_to_cart(part_id):
    part = Part.query.get_or_404(part_id)
    cart = session.get('cart', {})
    cart[str(part_id)] = cart.get(str(part_id), 0) + 1
    session['cart'] = cart
    flash('Part added to cart!', 'success')
    return redirect(url_for('catalogue'))

@app.route('/remove_from_cart/<int:part_id>', methods=['POST'])
@login_required
def remove_from_cart(part_id):
    cart = session.get('cart', {})
    part_id_str = str(part_id)
    if part_id_str in cart:
        del cart[part_id_str]
        session['cart'] = cart
        flash('Item removed from your cart!', 'success')
    else:
        flash('Item not found in your cart.', 'warning')
    return redirect(url_for('cart'))


@app.route('/cart', methods=['GET'])
@login_required
def cart():
    form = CartForm()  
    cart = session.get('cart', {})
    parts_in_cart = []
    total_price = 0
    for part_id, quantity in cart.items():
        part = Part.query.get(int(part_id))
        if part:
            parts_in_cart.append({'part': part, 'quantity': quantity})
            total_price += part.price * quantity
    
    # Get next order ID by looking at all orders in the system
    latest_order = Order.query.order_by(Order.id.desc()).first()
    next_order_id = (latest_order.id + 1) if latest_order else 1
    
    return render_template('cart.html', 
                         form=form, 
                         parts=parts_in_cart, 
                         total_price=total_price,
                         next_order_id=next_order_id)

@app.route('/purchase_cart', methods=['POST'])
@login_required
def purchase_cart():
    form = CartForm()
    if not form.validate_on_submit():
        flash('Please fill in all shipping information.', 'danger')
        return redirect(url_for('cart'))
    
    cart = session.get('cart', {})
    
    if not cart:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('cart'))

    # Get next order ID for the payment reference
    latest_order = Order.query.order_by(Order.id.desc()).first()
    next_order_id = (latest_order.id + 1) if latest_order else 1
    
    purchases_to_make = []
    total_amount = 0
    
    try:
        # Validate items and calculate total
        for part_id_str in cart.keys():
            part_id = int(part_id_str)
            quantity_key = f'quantities[{part_id}]'
            quantity = int(request.form.get(quantity_key, 1))
            
            if quantity < 1:
                flash('Quantity must be at least 1', 'danger')
                return redirect(url_for('cart'))
            
            part = Part.query.get(part_id)
            if not part:
                flash(f'Part not found.', 'danger')
                return redirect(url_for('cart'))
            
            if part.quantity < quantity:
                flash(f'Not enough stock for {part.name}.', 'danger')
                return redirect(url_for('cart'))
            
            subtotal = part.price * quantity
            total_amount += subtotal
            purchases_to_make.append({
                'part': part,
                'quantity': quantity,
                'total_price': subtotal
            })

        # Create new order with payment reference
        new_order = Order(
            id=next_order_id,  # Explicitly set the ID
            user_id=current_user.id,
            total_amount=total_amount,
            payment_status='pending',
            payment_reference=f'Order-{next_order_id}',
            shipping_name=form.shipping_name.data,
            shipping_address=form.shipping_address.data
        )
        db.session.add(new_order)
        db.session.flush()  # This gets us the order.id
        
        # Create purchases under this order
        for purchase_info in purchases_to_make:
            part = purchase_info['part']
            quantity = purchase_info['quantity']
            
            purchase = Purchase(
                order_id=new_order.id,
                part_id=part.id,
                user_id=current_user.id,
                quantity=quantity,
                total_price=purchase_info['total_price']
            )
            
            # Update part quantity
            part.quantity -= quantity
            part.update_availability()
            
            db.session.add(purchase)
        
        db.session.commit()
        session.pop('cart', None)
        flash(f'Order #{new_order.id} placed successfully! Please complete the bank transfer to process your order.', 'success')
        return redirect(url_for('my_orders'))

    except Exception as e:
        db.session.rollback()
        flash('An error occurred during the purchase.', 'danger')
        logger.error(f"Error during purchase: {str(e)}")
        return redirect(url_for('cart'))

@app.route('/my_orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).all()
    
    supplier_orders = []
    if current_user.role == 'supplier':
        supplier_orders = (Order.query
            .join(Purchase)
            .join(Part)
            .filter(Part.supplier_id == current_user.id)
            .order_by(Order.order_date.desc())
            .distinct()
            .all())    
    return render_template('my_orders.html', 
                         orders=orders,
                         supplier_orders=supplier_orders)

@app.route('/confirm_payment/<int:order_id>', methods=['POST'])
@login_required
def confirm_payment(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('You can only confirm payment for your own orders.', 'danger')
        return redirect(url_for('my_orders'))
    
    if order.payment_status == 'pending':
        order.payment_status = 'paid'
        db.session.commit()
        flash('Payment confirmed. Supplier has been notified to ship your order.', 'success')
    return redirect(url_for('my_orders'))

@app.route('/confirm_shipping/<int:order_id>', methods=['POST'])
@login_required
def confirm_shipping(order_id):
    order = Order.query.get_or_404(order_id)
    is_supplier = any(
        purchase.part.supplier_id == current_user.id 
        for purchase in order.purchases
    )
    
    if not is_supplier:
        flash('You can only confirm shipping for orders containing your parts.', 'danger')
        return redirect(url_for('my_orders'))
    
    if order.shipping_status == 'pending' and order.payment_status == 'paid':
        order.update_shipping_status('shipped')
        db.session.commit()
        flash('Shipping confirmed. Customer has been notified.', 'success')
    return redirect(url_for('my_orders'))

@app.route('/confirm_completion/<int:order_id>', methods=['POST'])
@login_required
def confirm_completion(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('You can only confirm completion for your own orders.', 'danger')
        return redirect(url_for('my_orders'))
    
    if order.completion_status == 'pending' and order.shipping_status == 'shipped':
        order.completion_status = 'completed'
        db.session.commit()
        flash('Order completion confirmed. Thank you for your purchase!', 'success')
    return redirect(url_for('my_orders'))

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/imprint')
def imprint():
    return render_template('imprint.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


# Main Execution
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
