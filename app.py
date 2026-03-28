from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    return "car"

app.run(host="0.0.0.0", port=5000)
