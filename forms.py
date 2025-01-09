from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, SelectField, 
                    FloatField, IntegerField, TextAreaField, FileField, EmailField)
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, NumberRange, Optional
import email_validator
from datetime import datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150)])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('customer', 'Customer'), ('supplier', 'Supplier')], validators=[InputRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class OfferPartForm(FlaskForm):
    name = StringField('Part Name', validators=[DataRequired()])
    manufacturer = StringField('Manufacturer', validators=[DataRequired()])  
    model = StringField('Model', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    availability = SelectField('Availability',
                             choices=[('In Stock', 'In Stock'),
                                    ('Out of Stock', 'Out of Stock'),
                                    ('Pre-order', 'Pre-order')],
                             validators=[DataRequired()])
    quantity = IntegerField('Quantity', 
                          validators=[InputRequired(), 
                                    NumberRange(min=0, message="Quantity must be 0 or greater")])
    delivery = SelectField('Estimated Delivery',
                         choices=[('1-2 business days', '1-2 business days'),
                                ('3-5 business days', '3-5 business days'),
                                ('1-2 weeks', '1-2 weeks'),
                                ('2-4 weeks', '2-4 weeks')],
                         validators=[DataRequired()])
    image = FileField('Part Image', validators=[Optional()])
    description = TextAreaField('Description', validators=[DataRequired()])

class ProfileForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), 
        Email()
    ])
    current_password = PasswordField('Current Password', validators=[
        DataRequired()
    ])
    new_password = PasswordField('New Password', validators=[
        Length(min=6, message="Password must be at least 6 characters long"),
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Update Profile')

class CartForm(FlaskForm):
    shipping_name = StringField('Full Name', validators=[DataRequired()])
    shipping_address = TextAreaField('Shipping Address', validators=[DataRequired()])
    submit = SubmitField('Place Order')
