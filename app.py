import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from db import db  # Import the db instance
from models import User  # Import the User model

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

# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('run_insert_sample'))

@app.route('/insert/sample')
def run_insert_sample():
    insert_sample()
    return 'Database flushed and populated with some sample data.'

# Sample data insertion function
def insert_sample():
    db.session.execute(db.delete(User))
    user1 = User(username='testuser1', email='test1@example.com', password='password123')
    user2 = User(username='testuser2', email='test2@example.com', password='password123')
    db.session.add_all([user1, user2])
    db.session.commit()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
