from flask import Flask, render_template, jsonify

app = Flask(__name__)

# In-memory product data (matches the featured produce shown on the home page)
# price: current price from the nearest/cheapest seller among multiple listings
# favorable: whether this is the best price available right now across sellers
# nearest_farmer_km: distance to the closest farmer selling this item
crops_db = [
    {
        "id": 1,
        "name": "Fresh Tomatoes",
        "category": "Vegetables",
        "price": "\u20b928",
        "unit": "kg",
        "favorable": True,
        "nearest_farmer_km": 1.8,
        "image": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=600&q=80"
    },
    {
        "id": 2,
        "name": "Organic Lettuce",
        "category": "Vegetables",
        "price": "\u20b935",
        "unit": "head",
        "favorable": True,
        "nearest_farmer_km": 2.4,
        "image": "https://images.unsplash.com/photo-1622206151226-18ca2c9d680b?w=600&q=80"
    },
    {
        "id": 3,
        "name": "Farm Fresh Eggs",
        "category": "Dairy",
        "price": "\u20b990",
        "unit": "dozen",
        "favorable": True,
        "nearest_farmer_km": 3.1,
        "image": "https://images.unsplash.com/photo-1518569656558-1f25e69d93d7?w=600&q=80"
    },
    {
        "id": 4,
        "name": "Hybrid Tomato Seeds",
        "category": "Seeds",
        "price": "\u20b9150",
        "unit": "packet",
        "favorable": True,
        "nearest_farmer_km": 4.6,
        "image": "https://images.unsplash.com/photo-1524598171353-e5643fdc4353?w=600&q=80"
    },
    {
        "id": 5,
        "name": "Fresh Organic Milk",
        "category": "Dairy",
        "price": "\u20b955",
        "unit": "litre",
        "favorable": True,
        "nearest_farmer_km": 1.2,
        "image": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=600&q=80"
    },
    {
        "id": 6,
        "name": "Seasonal Oranges",
        "category": "Seasonal",
        "price": "\u20b960",
        "unit": "kg",
        "favorable": True,
        "nearest_farmer_km": 5.3,
        "image": "https://images.unsplash.com/photo-1547514701-42782101795e?w=600&q=80"
    },
    {
        "id": 7,
        "name": "Fresh Blueberries",
        "category": "Fruits",
        "price": "\u20b9250",
        "unit": "box",
        "favorable": True,
        "nearest_farmer_km": 6.7,
        "image": "https://images.unsplash.com/photo-1498557850523-fd3d118b962e?w=600&q=80"
    },
    {
        "id": 8,
        "name": "Seasonal Mangoes",
        "category": "Seasonal",
        "price": "\u20b980",
        "unit": "kg",
        "favorable": True,
        "nearest_farmer_km": 3.9,
        "image": "https://images.unsplash.com/photo-1591073113125-e46713c829ed?w=600&q=80"
    }
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/crops', methods=['GET'])
def get_crops():
    return jsonify({"status": "success", "crops": crops_db})


if __name__ == '__main__':
    app.run(debug=True, port=5000)