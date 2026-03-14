from flask_sqlalchemy import SQLAlchemy
import stripe
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # pet_owner, adoption_agency, supplier
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    pets = db.relationship('Pet', backref='owner', lazy=True)
    adoption_listings = db.relationship('AdoptionListing', backref='agency', lazy=True)
    products = db.relationship('Product', backref='supplier', lazy=True)
    chat_messages = db.relationship('ChatMessage', backref='user', lazy=True)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)  # age in months
    gender = db.Column(db.String(10), nullable=False)
    weight = db.Column(db.Float)  # weight in kg
    medical_history = db.Column(db.Text)
    feeding_schedule = db.Column(db.Text)
    photo_filename = db.Column(db.String(200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AdoptionListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)  # age in months
    gender = db.Column(db.String(10), nullable=False)
    size = db.Column(db.String(20), nullable=False)  # small, medium, large
    description = db.Column(db.Text)
    vaccination_status = db.Column(db.String(50))
    spayed_neutered = db.Column(db.Boolean, default=False)
    good_with_kids = db.Column(db.Boolean, default=False)
    good_with_pets = db.Column(db.Boolean, default=False)
    adoption_fee = db.Column(db.Float, default=0)
    photo_filename = db.Column(db.String(200))
    is_available = db.Column(db.Boolean, default=True)
    agency_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # food, toys, accessories, etc.
    brand = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    pet_type = db.Column(db.String(50))  # dog, cat, bird, etc.
    photo_filename = db.Column(db.String(200))
    supplier_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20))
    customer_address = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False, default="COD")  # COD / UPI
    status = db.Column(db.String(20), default='pending')  # pending, processing, shipped, delivered
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # ✅ New column
    status = db.Column(db.String(20), default='pending')  # pending, processing, shipped, delivered


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_bot = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class AdoptionApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('adoption_listing.id'), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    applicant_name = db.Column(db.String(100), nullable=False)
    applicant_email = db.Column(db.String(120), nullable=False)
    applicant_phone = db.Column(db.String(20))
    experience_with_pets = db.Column(db.Text)
    living_situation = db.Column(db.String(100))  # apartment, house, etc.
    have_yard = db.Column(db.Boolean, default=False)
    other_pets = db.Column(db.Text)
    reason_for_adoption = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    response_date = db.Column(db.DateTime)
    agency_notes = db.Column(db.Text)
    
    # Relationships
    listing = db.relationship('AdoptionListing', backref='applications')
    applicant = db.relationship('User', backref='adoption_applications')

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')
    user = db.relationship('User', backref='cart')

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref='cart_items')

class FeedingReminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reminder_time = db.Column(db.String(10), nullable=False)  # Format: HH:MM
    food_type = db.Column(db.String(100))
    amount = db.Column(db.String(50))
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_sent = db.Column(db.DateTime)
    
    # Relationships
    pet = db.relationship('Pet', backref='feeding_reminders')
    owner = db.relationship('User', backref='feeding_reminders')
    
class VaccinationReminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    vaccine_name = db.Column(db.String(100), nullable=False)
    vaccination_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_sent = db.Column(db.DateTime)

    # Relationships
    pet = db.relationship('Pet', backref='vaccination_reminders')
    owner = db.relationship('User', backref='vaccination_reminders')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # email, system, reminder
    status = db.Column(db.String(20), default='sent')  # sent, delivered, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='notifications')

class VetAppointmentSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    vet_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    service_type = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    fee = db.Column(db.Float)
    max_patients = db.Column(db.Integer, default=1)
    booked_count = db.Column(db.Integer, default=0)

    status = db.Column(db.String(50), default="Available")

    image = db.Column(db.String(200))   # 👈 ADD THIS

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    vet = db.relationship('User', backref='vet_slots')


class VetAppointment(db.Model):
    __tablename__ = 'vet_appointment'

    id = db.Column(db.Integer, primary_key=True)

    slot_id = db.Column(db.Integer, db.ForeignKey('vet_appointment_slot.id'), nullable=False)
    pet_owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)  # ADD THIS

    status = db.Column(db.String(50), default="Booked")
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships
    slot = db.relationship('VetAppointmentSlot', backref='appointments')
    owner = db.relationship('User', backref='vet_appointments')
    pet = db.relationship('Pet', backref='vet_appointments')  # ADD THIS
    