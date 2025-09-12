from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField, BooleanField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    user_type = SelectField('Account Type', choices=[
        ('pet_owner', 'Pet Owner'),
        ('adoption_agency', 'Adoption Agency'),
        ('supplier', 'Pet Food Supplier')
    ], validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    address = TextAreaField('Address')

class PetForm(FlaskForm):
    name = StringField('Pet Name', validators=[DataRequired(), Length(min=1, max=100)])
    breed = StringField('Breed', validators=[DataRequired(), Length(min=1, max=100)])
    age = IntegerField('Age (in months)', validators=[DataRequired(), NumberRange(min=1, max=300)])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    weight = FloatField('Weight (kg)', validators=[NumberRange(min=0.1, max=200)])
    medical_history = TextAreaField('Medical History')
    feeding_schedule = TextAreaField('Feeding Schedule')
    photo = FileField('Pet Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])

class AdoptionListingForm(FlaskForm):
    pet_name = StringField('Pet Name', validators=[DataRequired(), Length(min=1, max=100)])
    breed = StringField('Breed', validators=[DataRequired(), Length(min=1, max=100)])
    age = IntegerField('Age (in months)', validators=[DataRequired(), NumberRange(min=1, max=300)])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    size = SelectField('Size', choices=[
        ('small', 'Small (under 10kg)'),
        ('medium', 'Medium (10-25kg)'),
        ('large', 'Large (over 25kg)')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    vaccination_status = StringField('Vaccination Status')
    spayed_neutered = BooleanField('Spayed/Neutered')
    good_with_kids = BooleanField('Good with Kids')
    good_with_pets = BooleanField('Good with Other Pets')
    adoption_fee = FloatField('Adoption Fee', validators=[NumberRange(min=0)])
    photo = FileField('Pet Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=1, max=200)])
    category = SelectField('Category', choices=[
        ('food', 'Food'),
        ('treats', 'Treats'),
        ('toys', 'Toys'),
        ('accessories', 'Accessories'),
        ('health', 'Health & Care'),
        ('training', 'Training Supplies')
    ], validators=[DataRequired()])
    brand = StringField('Brand', validators=[Length(max=100)])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    stock_quantity = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=0)])
    pet_type = SelectField('Pet Type', choices=[
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('fish', 'Fish'),
        ('small_animal', 'Small Animal'),
        ('all', 'All Pets')
    ], validators=[DataRequired()])
    photo = FileField('Product Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])

class OrderForm(FlaskForm):
    customer_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    customer_email = EmailField('Email', validators=[DataRequired(), Email()])
    customer_phone = StringField('Phone Number', validators=[Length(max=20)])
    customer_address = TextAreaField('Delivery Address', validators=[DataRequired()])