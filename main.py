import os
import uuid
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- MEMORY STORAGE (Temporary) ---
orders_db = {}

# --- THE "WOW" FACTOR TEMPLATE ---
# This includes Swiper.js, Animations, and Glassmorphism
VALENTINE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>For {{ partner }}</title>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&family=Great+Vibes&display=swap" rel="stylesheet">

    <style>
        /* --- DESIGN DNA --- */
        :root { --primary: #ff4d6d; --bg: #0f0c29; --glass: rgba(255, 255, 255, 0.1); }

        body { 
            margin: 0; font-family: 'Outfit', sans-serif; 
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            height: 100vh; display: flex; justify-content: center; align-items: center; 
            overflow: hidden; color: white;
        }

        /* DEVICE FRAME */
        .phone-frame {
            width: 100%; max-width: 400px; height: 100vh; max-height: 800px;
            background: black; position: relative; overflow: hidden;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }
        @media (min-width: 600px) {
            .phone-frame { height: 700px; border-radius: 30px; border: 10px solid #222; }
        }

        /* SLIDES */
        .swiper { width: 100%; height: 100%; }
        .swiper-slide { 
            display: flex; flex-direction: column; justify-content: center; align-items: center; 
            text-align: center; padding: 40px; box-sizing: border-box;
            background: linear-gradient(to bottom, #ff9a9e, #fecfef); color: #d63384;
        }

        /* TYPOGRAPHY */
        h1 { font-family: 'Great Vibes', cursive; font-size: 4rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); }
        p { font-size: 1.2rem; line-height: 1.6; font-weight: 500; }
        small { opacity: 0.8; margin-top: 20px; display: block; letter-spacing: 2px; text-transform: uppercase; font-size: 0.8rem; }

        /* ANIMATED HEART */
        .heart-beat { font-size: 5rem; animation: pulse 1.5s infinite; margin: 20px 0; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }

        /* MUSIC PLAYER BUTTON */
        .music-btn {
            position: absolute; bottom: 30px; right: 30px; z-index: 100;
            width: 50px; height: 50px; background: rgba(255,255,255,0.2);
            border-radius: 50%; display: flex; justify-content: center; align-items: center;
            backdrop-filter: blur(10px); cursor: pointer; border: 1px solid rgba(255,255,255,0.4);
        }
    </style>
</head>
<body>

    <div class="phone-frame">
        <div class="swiper mySwiper">
            <div class="swiper-wrapper">

                <div class="swiper-slide">
                    <div class="animate__animated animate__fadeInDown">
                        <p>A special message for</p>
                        <h1>{{ partner }}</h1>
                    </div>
                </div>

                <div class="swiper-slide">
                    <div class="heart-beat">❤️</div>
                    <p class="animate__animated animate__zoomIn" style="font-size: 1.5rem;">
                        "Every moment with you is magic."
                    </p>
                </div>

                <div class="swiper-slide">
                    <p class="animate__animated animate__fadeInUp" style="white-space: pre-wrap;">{{ message }}</p>
                    <small>With Love, {{ user }}</small>
                </div>

            </div>
            <div class="swiper-pagination"></div>
        </div>

        <div class="music-btn">🎵</div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>
        var swiper = new Swiper(".mySwiper", {
            effect: "cube",
            grabCursor: true,
            cubeEffect: {
                shadow: true, slideShadows: true, shadowOffset: 20, shadowScale: 0.94,
            },
            pagination: { el: ".swiper-pagination" },
        });
    </script>
</body>
</html>
"""


@app.route('/')
def home():
    return "✅ WebWish Factory is Online!"


@app.route('/create-wish', methods=['POST'])
def create_wish():
    try:
        data = request.json
        wish_id = str(uuid.uuid4())[:8]

        # Save Order
        orders_db[wish_id] = {
            "partner": data.get('partner_name', 'My Love'),
            "user": data.get('user_name', 'Admirer'),
            "message": data.get('message', 'Happy Valentine!')
        }

        return jsonify({
            "status": "success",
            "message": "3D Website Generated!",
            "redirect_url": f"https://webwish-api.onrender.com/w/{wish_id}"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/w/<wish_id>')
def view_wish(wish_id):
    order = orders_db.get(wish_id)
    if not order: return "❌ Expired or Invalid Link."

    # Inject data into the 3D Template
    return render_template_string(
        VALENTINE_TEMPLATE,
        partner=order['partner'],
        user=order['user'],
        message=order['message']
    )


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)