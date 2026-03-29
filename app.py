from flask import Flask, request
import numpy as np
import cv2

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    image_data = request.data
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    height, width, _ = img.shape

    # Divide image
    left = img[:, :width//3]
    center = img[:, width//3:2*width//3]
    right = img[:, 2*width//3:]

    def analyze(region):
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return np.sum(edges)

    scores = {
        "LEFT": analyze(left),
        "CENTER": analyze(center),
        "RIGHT": analyze(right)
    }

    direction = max(scores, key=scores.get)
    score = scores[direction]

    # Object classification (improved logic)
    if score > 70000:
        obj = "wall"
    elif score > 40000:
        obj = "car"
    elif score > 20000:
        obj = "obstacle"
    else:
        obj = "person"

    # Fake distance estimation (camera-based)
    if score > 70000:
        distance = "2-3 meters"
    elif score > 40000:
        distance = "3-6 meters"
    else:
        distance = "6-10 meters"

    return f"{obj} detected {direction} at approx {distance}"

if __name__ == "__main__":
    app.run()
