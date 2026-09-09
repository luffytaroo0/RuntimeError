from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLite for easy local development
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category_rel.name if self.category_rel else "General",
            "price": self.price,
            "unit": self.unit,
            "favorable": self.favorable,
            "nearest_farmer_km": self.nearest_farmer_km,
            "image": self.image
        }

# --- Seed Initial Data ---
def seed_data():
    if not Category.query.first():
        print("Seeding initial database categories and products...")
        cat_veg = Category(name='Vegetables')
        cat_fruit = Category(name='Fruits')
        cat_dairy = Category(name='Dairy')
        cat_seeds = Category(name='Seeds')
        cat_seasonal = Category(name='Seasonal')
        
        db.session.add_all([cat_veg, cat_fruit, cat_dairy, cat_seeds, cat_seasonal])
        db.session.commit()

        initial_crops = [
            Product(name="Fresh Tomatoes", category_id=cat_veg.id, price="₹28", unit="kg", favorable=True, nearest_farmer_km=1.8, image="https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=600&q=80"),
            Product(name="Organic Lettuce", category_id=cat_veg.id, price="₹35", unit="head", favorable=True, nearest_farmer_km=2.4, image="https://images.unsplash.com/photo-1622206151226-18ca2c9d680b?w=600&q=80"),
            Product(name="Farm Fresh Eggs", category_id=cat_dairy.id, price="₹90", unit="dozen", favorable=True, nearest_farmer_km=3.1, image="https://images.unsplash.com/photo-1518569656558-1f25e69d93d7?w=600&q=80"),
            Product(name="Hybrid Tomato Seeds", category_id=cat_seeds.id, price="₹150", unit="packet", favorable=True, nearest_farmer_km=4.6, image="https://images.unsplash.com/photo-1524598171353-e5643fdc4353?w=600&q=80"),
            Product(name="Fresh Organic Milk", category_id=cat_dairy.id, price="₹55", unit="litre", favorable=True, nearest_farmer_km=1.2, image="https://images.unsplash.com/photo-1563636619-e9143da7973b?w=600&q=80"),
            Product(name="Seasonal Oranges", category_id=cat_seasonal.id, price="₹60", unit="kg", favorable=True, nearest_farmer_km=5.3, image="https://images.unsplash.com/photo-1547514701-42782101795e?w=600&q=80"),
            Product(name="Fresh Blueberries", category_id=cat_fruit.id, price="₹250", unit="box", favorable=True, nearest_farmer_km=6.7, image="https://images.unsplash.com/photo-1498557850523-fd3d118b962e?w=600&q=80"),
            Product(name="Seasonal Mangoes", category_id=cat_seasonal.id, price="₹80", unit="kg", favorable=True, nearest_farmer_km=3.9, image="https://images.unsplash.com/photo-1591073113125-e46713c829ed?w=600&q=80")
        ]
        db.session.add_all(initial_crops)
        db.session.commit()

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/crops', methods=['GET'])
def get_crops():
    crops = Product.query.all()
    return jsonify({
        "status": "success", 
        "crops": [crop.to_dict() for crop in crops]
    })

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

# THIS IS THE ROUTE THAT WAS MISSING OR UNSAVED
@app.route('/product/<int:product_id>/seller/<seller_name>')
def seller_listing(product_id, seller_name):
    product = Product.query.get_or_404(product_id)
    return render_template('seller_listing.html', product=product, seller_name=seller_name)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
        seed_data()      
    app.run(debug=True, port=5000)