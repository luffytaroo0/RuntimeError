from flask import Flask, render_template, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os

app = Flask(__name__)
app.secret_key = 'super_secret_college_project_key'

# Using v3 to guarantee a completely fresh, unbroken database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///अन्नData_v3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
server_otp_storage = {} 

# --- Database Models ---
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    products = db.relationship('Product', backref='category_rel', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    price = db.Column(db.String(20), nullable=False) 
    unit = db.Column(db.String(20), nullable=False) 
    favorable = db.Column(db.Boolean, default=True)
    nearest_farmer_km = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=True)
    seller_name = db.Column(db.String(100), default="Local Farm")
    stock = db.Column(db.Integer, default=0)
    self_delivery = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category_rel.name if self.category_rel else "General",
            "price": self.price,
            "unit": self.unit,
            "favorable": self.favorable,
            "nearest_farmer_km": self.nearest_farmer_km,
            "image": self.image,
            "seller_name": self.seller_name,
            "stock": self.stock
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=True) 
    address = db.Column(db.Text, nullable=True)
    is_seller = db.Column(db.Boolean, default=False)
    kisaan_id = db.Column(db.String(10), unique=True, nullable=True)

class ValidKisaan(db.Model):
    __tablename__ = 'valid_kisaan_ids'
    id = db.Column(db.Integer, primary_key=True)
    kisaan_id = db.Column(db.String(5), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False) 
    name = db.Column(db.String(100), nullable=False)

# --- Seed Initial Data ---
def seed_data():
    db.create_all()
    if not Category.query.first():
        cat_veg = Category(name='Vegetables')
        cat_fruit = Category(name='Fruits')
        cat_dairy = Category(name='Dairy')
        cat_seasonal = Category(name='Seasonal')
        cat_seeds = Category(name='Seeds')
        db.session.add_all([cat_veg, cat_fruit, cat_dairy, cat_seeds, cat_seasonal])
        db.session.commit()

        initial_crops = [
            Product(name="Fresh Tomatoes", category_id=cat_veg.id, price="₹28", unit="kg", nearest_farmer_km=1.8, image="https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=600&q=80", seller_name="Ramesh Kumar", stock=50),
            Product(name="Farm Fresh Eggs", category_id=cat_dairy.id, price="₹90", unit="dozen", nearest_farmer_km=3.1, image="https://images.unsplash.com/photo-1518569656558-1f25e69d93d7?w=600&q=80", seller_name="Suresh Singh", stock=20)
        ]
        db.session.add_all(initial_crops)
        db.session.commit()

    if not ValidKisaan.query.first():
        db.session.add_all([
            ValidKisaan(kisaan_id="12345", email="farmer1@test.com", name="Ramesh Kumar"),
            ValidKisaan(kisaan_id="67890", email="farmer2@test.com", name="Suresh Singh")
        ])
        db.session.commit()

# --- UI Routes ---
@app.route('/')
def index(): return render_template('index.html')

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    return render_template('product_detail.html', product=Product.query.get_or_404(product_id))

@app.route('/product/<int:product_id>/seller/<seller_name>')
def seller_listing(product_id, seller_name):
    return render_template('seller_listing.html', product=Product.query.get_or_404(product_id), seller_name=seller_name)

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    crops = Product.query.filter(Product.name.ilike(f'%{query}%')).all() if query else []
    return render_template('search_results.html', crops=crops, query=query)

# --- API Routes ---
@app.route('/api/crops', methods=['GET'])
def get_crops():
    try:
        return jsonify({"status": "success", "crops": [c.to_dict() for c in Product.query.all()]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/sell_item', methods=['POST'])
def add_product():
    if not session.get('is_seller'):
        return jsonify({"status": "error", "message": "Unauthorized. You must be a logged-in seller."}), 401
    
    data = request.json
    category = Category.query.filter_by(name=data['category']).first()
    if not category: category = Category.query.filter_by(name='Vegetables').first()

    img_map = {
        'onion': 'https://images.unsplash.com/photo-1620574387735-3624d75b2dbc?w=600&q=80',
        'potato': 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=600&q=80',
        'milk': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=600&q=80',
        'banana': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=600&q=80'
    }
    img_url = img_map.get(data['sub_category'].lower(), 'https://images.unsplash.com/photo-1595856424599-28c1192e4242?w=600&q=80')

    new_prod = Product(
        name=data['sub_category'].title(), category_id=category.id, price=f"₹{data['final_price']}",
        unit=data['unit'], stock=int(data['stock']), self_delivery=data['self_delivery'],
        seller_name=session.get('user_name'), nearest_farmer_km=round(random.uniform(1.0, 10.0), 1), image=img_url
    )
    db.session.add(new_prod)
    db.session.commit()
    return jsonify({"status": "success", "message": "Item listed successfully!"})

@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    return jsonify({"logged_in": 'user_id' in session, "name": session.get('user_name'), "is_seller": session.get('is_seller', False)})

@app.route('/api/auth/generate_otp', methods=['POST'])
def generate_otp():
    kisaan_id = request.json.get('kisaan_id')
    valid_farmer = ValidKisaan.query.filter_by(kisaan_id=kisaan_id).first()
    if not valid_farmer: return jsonify({"status": "error", "message": "Invalid Kisaan ID"}), 400
    
    otp = str(random.randint(100000, 999999))
    server_otp_storage[kisaan_id] = otp
    print("\n" + "="*50 + f"\n📧 SENDING OTP TO: {valid_farmer.email}\n🔑 YOUR OTP IS: {otp}\n" + "="*50 + "\n")
    return jsonify({"status": "success", "message": f"OTP sent to {valid_farmer.email}!"})

@app.route('/api/auth/verify_seller', methods=['POST'])
def verify_seller():
    data = request.json
    kisaan_id, otp = data.get('kisaan_id'), data.get('otp')
    if kisaan_id not in server_otp_storage or server_otp_storage[kisaan_id] != otp:
        return jsonify({"status": "error", "message": "Invalid OTP"}), 401
    
    del server_otp_storage[kisaan_id]
    valid_farmer = ValidKisaan.query.filter_by(kisaan_id=kisaan_id).first()
    user = User.query.filter_by(kisaan_id=kisaan_id).first()
    if not user:
        user = User(name=valid_farmer.name, email=valid_farmer.email, is_seller=True, kisaan_id=kisaan_id)
        db.session.add(user)
        db.session.commit()
    
    session['user_id'], session['user_name'], session['is_seller'] = user.id, user.name, True
    return jsonify({"status": "success", "message": f"Welcome Seller, {user.name}!"})

if __name__ == '__main__':
    with app.app_context(): seed_data()      
    app.run(debug=True, port=5000)