import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- CONFIGURATION ---
app = Flask(__name__)
CORS(app)  # This is CRITICAL. It allows your Framer/Netlify site to talk to this server.


# --- THE WELCOME MAT ---
@app.route('/')
def home():
    return "✅ WebWish Factory is Online! The Engine is Purring."


# --- THE ORDER RECEIVER ---
@app.route('/create-wish', methods=['POST'])
def create_wish():
    try:
        # 1. Get Data from the Editor
        data = request.json
        print(f"📦 New Order Received: {data}")

        # 2. Extract Details (We will use these later for the build)
        template_id = data.get('template_id')
        partner_name = data.get('partner_name', 'Partner')
        user_name = data.get('user_name', 'User')

        # --- FUTURE LOGIC: GENERATE WEBSITE HERE ---
        # For now, we just confirm we got it.

        # 3. Send Success Response
        return jsonify({
            "status": "success",
            "message": "Order Received!",
            "redirect_url": "https://webwish.in/thank-you"  # We will change this later
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# --- START THE SERVER ---
if __name__ == '__main__':
    # This allows it to run on Render (port 10000) or Laptop (port 5000)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)