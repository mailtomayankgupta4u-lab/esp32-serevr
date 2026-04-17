from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

latest_text = "System started"

# Twilio config
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
USER_NUMBER = os.getenv("USER_NUMBER")

def send_sms(msg):
    try:
        requests.post(
            f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json",
            auth=(TWILIO_SID, TWILIO_AUTH),
            data={
                "From": TWILIO_NUMBER,
                "To": USER_NUMBER,
                "Body": msg
            }
        )
    except:
        print("SMS failed")

@app.route('/')
def home():
    return "Server Running ✅"

@app.route('/process', methods=['POST'])
def process():
    global latest_text

    # 🔥 Replace later with real AI
    latest_text = "Obstacle detected in front"

    # Emergency condition
    if "obstacle" in latest_text.lower():
        send_sms("⚠️ ALERT: Obstacle detected!")

    return jsonify({"status": "ok", "text": latest_text})

@app.route('/get_text', methods=['GET'])
def get_text():
    return jsonify({"text": latest_text})

if __name__ == "__main__":
    app.run()
