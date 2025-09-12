import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from models import db, User, Pet, AdoptionListing, Product, Order, ChatMessage
from forms import LoginForm, RegisterForm, PetForm, AdoptionListingForm, ProductForm, OrderForm
from gemini import get_pet_advice
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///petcare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def api_health():
    return {'status': 'ok', 'message': 'Pet Care Connect API is running'}, 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password_hash and check_password_hash(user.password_hash, form.password.data or ''):
            session['user_id'] = user.id
            session['user_type'] = user.user_type
            flash('Login successful!', 'success')
            
            if user.user_type == 'pet_owner':
                return redirect(url_for('pet_owner_dashboard'))
            elif user.user_type == 'adoption_agency':
                return redirect(url_for('agency_dashboard'))
            elif user.user_type == 'supplier':
                return redirect(url_for('supplier_dashboard'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered', 'error')
        else:
            user = User()
            user.name = form.name.data or ''
            user.email = form.email.data or ''
            user.password_hash = generate_password_hash(form.password.data or '')
            user.user_type = form.user_type.data or ''
            user.phone = form.phone.data or ''
            user.address = form.address.data or ''
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/pet-owner-dashboard')
def pet_owner_dashboard():
    if 'user_id' not in session or session['user_type'] != 'pet_owner':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('login'))
    pets = Pet.query.filter_by(owner_id=user.id).all()
    return render_template('pet_owner_dashboard.html', user=user, pets=pets)

@app.route('/agency-dashboard')
def agency_dashboard():
    if 'user_id' not in session or session['user_type'] != 'adoption_agency':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('login'))
    listings = AdoptionListing.query.filter_by(agency_id=user.id).all()
    return render_template('agency_dashboard.html', user=user, listings=listings)

@app.route('/supplier-dashboard')
def supplier_dashboard():
    if 'user_id' not in session or session['user_type'] != 'supplier':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('login'))
    products = Product.query.filter_by(supplier_id=user.id).all()
    orders = Order.query.join(Product).filter(Product.supplier_id == user.id).all()
    return render_template('supplier_dashboard.html', user=user, products=products, orders=orders)

@app.route('/add-adoption-listing', methods=['GET', 'POST'])
def add_adoption_listing():
    if 'user_id' not in session or session['user_type'] != 'adoption_agency':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    form = AdoptionListingForm()
    if form.validate_on_submit():
        filename = None
        if form.photo.data:
            filename = secure_filename(f"{uuid.uuid4().hex}_{form.photo.data.filename}")
            form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        listing = AdoptionListing()
        listing.pet_name = form.pet_name.data or ''
        listing.breed = form.breed.data or ''
        listing.age = form.age.data or 0
        listing.gender = form.gender.data or ''
        listing.size = form.size.data or ''
        listing.description = form.description.data or ''
        listing.vaccination_status = form.vaccination_status.data or ''
        listing.spayed_neutered = form.spayed_neutered.data
        listing.good_with_kids = form.good_with_kids.data
        listing.good_with_pets = form.good_with_pets.data
        listing.adoption_fee = form.adoption_fee.data or 0
        listing.photo_filename = filename
        listing.agency_id = session['user_id']
        
        db.session.add(listing)
        db.session.commit()
        flash('Pet listing added successfully!', 'success')
        return redirect(url_for('agency_dashboard'))
    
    return render_template('add_adoption_listing.html', form=form)

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session or session['user_type'] != 'supplier':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    form = ProductForm()
    if form.validate_on_submit():
        filename = None
        if form.photo.data:
            filename = secure_filename(f"{uuid.uuid4().hex}_{form.photo.data.filename}")
            form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        product = Product()
        product.name = form.name.data or ''
        product.category = form.category.data or ''
        product.brand = form.brand.data or ''
        product.description = form.description.data or ''
        product.price = form.price.data or 0
        product.stock_quantity = form.stock_quantity.data or 0
        product.pet_type = form.pet_type.data or ''
        product.photo_filename = filename
        product.supplier_id = session['user_id']
        
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('supplier_dashboard'))
    
    return render_template('add_product.html', form=form)

@app.route('/add-pet', methods=['GET', 'POST'])
def add_pet():
    if 'user_id' not in session or session['user_type'] != 'pet_owner':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    form = PetForm()
    if form.validate_on_submit():
        filename = None
        if form.photo.data:
            filename = secure_filename(f"{uuid.uuid4().hex}_{form.photo.data.filename}")
            form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        pet = Pet()
        pet.name = form.name.data or ''
        pet.breed = form.breed.data or ''
        pet.age = form.age.data or 0
        pet.gender = form.gender.data or ''
        pet.weight = form.weight.data or 0
        pet.medical_history = form.medical_history.data or ''
        pet.feeding_schedule = form.feeding_schedule.data or ''
        pet.photo_filename = filename
        pet.owner_id = session['user_id']
        db.session.add(pet)
        db.session.commit()
        flash('Pet added successfully!', 'success')
        return redirect(url_for('pet_owner_dashboard'))
    
    return render_template('add_pet.html', form=form)

@app.route('/browse-pets')
def browse_pets():
    page = request.args.get('page', 1, type=int)
    breed_filter = request.args.get('breed', '')
    size_filter = request.args.get('size', '')
    
    query = AdoptionListing.query.filter_by(is_available=True)
    
    if breed_filter:
        query = query.filter(AdoptionListing.breed.contains(breed_filter))
    
    if size_filter:
        query = query.filter(AdoptionListing.size == size_filter)
    
    listings = query.paginate(page=page, per_page=12, error_out=False)
    return render_template('browse_pets.html', listings=listings, breed_filter=breed_filter, size_filter=size_filter)

@app.route('/chatbot')
def chatbot():
    if 'user_id' not in session or session['user_type'] != 'pet_owner':
        flash('Chatbot is only available for pet owners', 'error')
        return redirect(url_for('login'))
    
    messages = ChatMessage.query.filter_by(user_id=session['user_id']).order_by(ChatMessage.timestamp).all()
    return render_template('chatbot.html', messages=messages)

@app.route('/chat', methods=['POST'])
def chat():
    if 'user_id' not in session or session['user_type'] != 'pet_owner':
        return jsonify({'error': 'Access denied'}), 403
    
    user_message = (request.json or {}).get('message', '').strip()
    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    # Save user message
    user_chat = ChatMessage()
    user_chat.user_id = session['user_id']
    user_chat.message = user_message
    user_chat.is_bot = False
    db.session.add(user_chat)
    
    try:
        # Get AI response
        bot_response = get_pet_advice(user_message)
        
        # Save bot response
        bot_chat = ChatMessage()
        bot_chat.user_id = session['user_id']
        bot_chat.message = bot_response
        bot_chat.is_bot = True
        db.session.add(bot_chat)
        db.session.commit()
        
        return jsonify({
            'user_message': user_message,
            'bot_response': bot_response
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Sorry, I am unable to respond right now. Please try again later.'}), 500

@app.route('/edit-pet/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    pet = Pet.query.filter_by(id=pet_id, owner_id=session['user_id']).first_or_404()
    form = PetForm(obj=pet)
    
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.breed = form.breed.data
        pet.age = form.age.data
        pet.weight = form.weight.data
        pet.gender = form.gender.data
        pet.medical_history = form.medical_history.data
        pet.feeding_schedule = form.feeding_schedule.data
        
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            filename = f"{uuid.uuid4().hex}_{filename}"
            form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pet.photo_filename = filename
        
        db.session.commit()
        flash('Pet updated successfully!', 'success')
        return redirect(url_for('pet_owner_dashboard'))
    
    return render_template('add_pet.html', form=form, edit_mode=True)

@app.route('/edit-listing/<int:listing_id>', methods=['GET', 'POST'])
def edit_listing(listing_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    listing = AdoptionListing.query.filter_by(id=listing_id, agency_id=session['user_id']).first_or_404()
    form = AdoptionListingForm(obj=listing)
    
    if form.validate_on_submit():
        listing.pet_name = form.pet_name.data
        listing.species = form.species.data
        listing.breed = form.breed.data
        listing.age = form.age.data
        listing.gender = form.gender.data
        listing.size = form.size.data
        listing.description = form.description.data
        listing.vaccination_status = form.vaccination_status.data
        listing.spayed_neutered = form.spayed_neutered.data
        listing.good_with_kids = form.good_with_kids.data
        listing.good_with_pets = form.good_with_pets.data
        listing.adoption_fee = form.adoption_fee.data
        
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            filename = f"{uuid.uuid4().hex}_{filename}"
            form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            listing.photo_filename = filename
        
        db.session.commit()
        flash('Listing updated successfully!', 'success')
        return redirect(url_for('agency_dashboard'))
    
    return render_template('add_adoption_listing.html', form=form, edit_mode=True)

@app.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    product = Product.query.filter_by(id=product_id, supplier_id=session['user_id']).first_or_404()
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.category = form.category.data
        product.brand = form.brand.data
        product.pet_type = form.pet_type.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock_quantity = form.stock_quantity.data
        
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            filename = f"{uuid.uuid4().hex}_{filename}"
            form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.photo_filename = filename
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('supplier_dashboard'))
    
    return render_template('add_product.html', form=form, edit_mode=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)