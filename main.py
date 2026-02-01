import os
import uuid
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
# Allow everyone to talk to us (CORS)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- 1. MEMORY STORAGE (Temporary) ---
# In a real startup, we use a Database (Day 5).
# For now, we keep orders in the server's RAM.
orders_db = {}

# --- 2. HTML TEMPLATE (The Product) ---
# This is the "Base Design" that gets filled with user data.
VALENTINE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>For {{ partner }}</title>
    <style>
        body { background: #ff9a9e; color: white; text-align: center; font-family: sans-serif; display: flex; flex-direction: column; justify-content: center; height: 100vh; margin: 0; }
        h1 { font-size: 3rem; margin-bottom: 10px; }
        p { font-size: 1.5rem; }
        .card { background: rgba(255,255,255,0.2); padding: 40px; border-radius: 20px; display: inline-block; margin: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>❤️ {{ partner }} ❤️</h1>
        <p>{{ message }}</p>
        <br>
        <small>With love from, {{ user }}</small>
    </div>
</body>
</html>
"""


@app.route('/')
def home():
    return "✅ WebWish Factory is Online!"


# --- 3. CREATE WISH (The Input) ---
@app.route('/create-wish', methods=['POST'])
def create_wish():
    try:
        data = request.json

        # generate a unique ID (e.g., 'a1b2c3d4')
        wish_id = str(uuid.uuid4())[:8]

        # Save to our "Database"
        orders_db[wish_id] = {
            "partner": data.get('partner_name', 'My Love'),
            "user": data.get('user_name', 'Admirer'),
            "message": data.get('message', 'Happy Valentine!')
        }

        print(f"📦 Created Wish {wish_id} for {data.get('user_name')}")

        # Return the unique link
        return jsonify({
            "status": "success",
            "message": "Website Generated!",
            "redirect_url": f"https://webwish-api.onrender.com/w/{wish_id}"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# --- 4. VIEW WISH (The Output) ---
@app.route('/w/<wish_id>')
def view_wish(wish_id):
    # Find the order in our database
    order = orders_db.get(wish_id)

    if not order:
        return "❌ Oops! This wish doesn't exist or has expired."

    # Inject the data into the HTML
    return render_template_string(
        VALENTINE_TEMPLATE,
        partner=order['partner'],
        user=order['user'],
        message=order['message']
    )


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)