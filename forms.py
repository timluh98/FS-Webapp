from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, SelectField, 
                    FloatField, IntegerField, TextAreaField, FileField, EmailField, DateField)
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, NumberRange
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
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    delivery = SelectField('Estimated Delivery',
                         choices=[('1-2 business days', '1-2 business days'),
                                ('3-5 business days', '3-5 business days'),
                                ('1-2 weeks', '1-2 weeks'),
                                ('2-4 weeks', '2-4 weeks')],
                         validators=[DataRequired()])
    image = FileField('Part Image', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

class PurchaseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    card_number = StringField('Card Number', validators=[DataRequired()])
    cvc = StringField('CVC', validators=[DataRequired(), Length(max=4)])
    exp_month = SelectField('Expiration Month', 
    choices=[('', 'Month')] + [(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)], validators=[DataRequired()])
    current_year = datetime.now().year
    exp_year = SelectField('Expiration Year',
    choices=[('', 'Year')] + [(str(y), str(y)) for y in range(current_year, current_year + 21)], validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Purchase')

class ProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[EqualTo('new_password')])
    submit = SubmitField('Update Profile')

