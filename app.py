from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Mock In-Memory Database for Hackathon Prototype
crops_db = [
    {
        "id": 1,
        "name": "Fresh Tomatoes",
        "category": "vegetables",
        "farmer": "Ramesh Kumar",
        "farmer_id": "487-8942-12",
        "price": 28,
        "mandi_price": 45,
        "qty": "120 kg",
        "image": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400"
    },
    {
        "id": 2,
        "name": "Organic Lettuce",
        "category": "vegetables",
        "farmer": "Suresh Patel",
        "farmer_id": "487-1102-88",
        "price": 35,
        "mandi_price": 55,
        "qty": "45 kg",
        "image": "https://images.unsplash.com/photo-1556801712-76c8eb07bbc9?w=400"
    },
    {
        "id": 3,
        "name": "Fresh Organic Milk",
        "category": "dairy",
        "farmer": "Dairy FPO Meerut",
        "farmer_id": "487-3391-04",
        "price": 52,
        "mandi_price": 68,
        "qty": "80 L",
        "image": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400"
    },
    {
        "id": 4,
        "name": "Whole Wheat Grain",
        "category": "grains",
        "farmer": "Ramesh Kumar",
        "farmer_id": "487-8942-12",
        "price": 24,
        "mandi_price": 34,
        "qty": "500 kg",
        "image": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400"
    }
]

orders_db = []

@app.route('/')
def index():
    return render_template('index.html')

# API: Get all crops
@app.route('/api/crops', methods=['GET'])
def get_crops():
    return jsonify({"status": "success", "crops": crops_db})

# API: Add new crop listing by farmer
@app.route('/api/crops', methods=['POST'])
def add_crop():
    data = request.get_json()
    new_crop = {
        "id": len(crops_db) + 1,
        "name": data.get("name"),
        "category": data.get("category", "vegetables"),
        "farmer": data.get("farmer", "Sarah Jenkins"),
        "farmer_id": "487-8942-12",
        "price": float(data.get("price")),
        "mandi_price": round(float(data.get("price")) * 1.4, 1),
        "qty": f"{data.get('qty')} kg",
        "image": data.get("image") or "https://images.unsplash.com/photo-1542838132-92c53300491e?w=400"
    }
    crops_db.insert(0, new_crop)
    return jsonify({"status": "success", "message": "Crop listed successfully!", "crop": new_crop})

# API: Simulated AI Price & Demand Suggester
@app.route('/api/ai-forecast', methods=['POST'])
def ai_forecast():
    data = request.get_json()
    crop_name = data.get("crop_name", "").lower()
    
    # Fast deterministic rules for demo
    if "tomato" in crop_name:
        rec_price = 28
        demand = "High (Monsoon deficit in regional mandis)"
    elif "wheat" in crop_name:
        rec_price = 25
        demand = "Stable (Bulk procurement season active)"
    else:
        rec_price = 32
        demand = "Moderate demand. Direct consumer pricing suggested."

    return jsonify({
        "status": "success",
        "recommended_price": rec_price,
        "demand_forecast": demand
    })

# API: Place direct order
@app.route('/api/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    order = {
        "order_id": f"ORD-2026-{len(orders_db) + 101}",
        "crop_name": data.get("crop_name"),
        "farmer": data.get("farmer"),
        "amount": data.get("price"),
        "status": "Logistics Dispatched"
    }
    orders_db.append(order)
    return jsonify({"status": "success", "order": order})

if __name__ == '__main__':
    app.run(debug=True, port=5000)