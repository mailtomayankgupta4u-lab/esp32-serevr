from flask import Flask, request, jsonify
import openai
import requests
import os

app = Flask(__name__)

# API KEYS
openai.api_key = os.getenv("OPENAI_API_KEY")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
USER_NUMBER = os.getenv("USER_NUMBER")

ELEVEN_API = os.getenv("ELEVEN_API")

# 🔷 MAIN API
@app.route('/process', methods=['POST'])
def process():

    data = request.json
    detected_object = data.get("object", "unknown")
    pulse = data.get("pulse", 70)
    danger = data.get("danger", False)

    # 🔥 AI TEXT GENERATION
    ai_response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Describe danger: {detected_object}"}
        ]
    )

    text = ai_response['choices'][0]['message']['content']

    # 🔥 DECISION ENGINE
    emergency = False
    if pulse > 110 or danger:
        emergency = True

    # 🔥 SMS ALERT
    if emergency:
        requests.post(
            f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json",
            auth=(TWILIO_SID, TWILIO_AUTH),
            data={
                "From": TWILIO_NUMBER,
                "To": USER_NUMBER,
                "Body": f"Emergency! {text}"
            }
        )

    # 🔥 TEXT TO SPEECH
    tts_response = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech",
        headers={
            "xi-api-key": ELEVEN_API,
            "Content-Type": "application/json"
        },
        json={
            "text": text,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
        }
    )

    audio_url = "https://your-server/audio/latest.mp3"  # placeholder

    return jsonify({
        "text": text,
        "audio": audio_url,
        "emergency": emergency
    })

if __name__ == "__main__":
    app.run()
