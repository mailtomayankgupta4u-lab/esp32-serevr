from flask import Flask, request
import numpy as np
import cv2

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    distance = request.headers.get("Distance")

    image_data = request.data
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    height, width, _ = img.shape

    # Divide into 3 vertical regions
    left = img[:, :width//3]
    center = img[:, width//3:2*width//3]
    right = img[:, 2*width//3:]

    def detect_region(region):
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return np.sum(edges)

    left_score = detect_region(left)
    center_score = detect_region(center)
    right_score = detect_region(right)

    # Decide direction
    if left_score > center_score and left_score > right_score:
        direction = "LEFT"
        score = left_score
    elif right_score > center_score:
        direction = "RIGHT"
        score = right_score
    else:
        direction = "CENTER"
        score = center_score

    # Object detection (basic logic)
    if score > 50000:
        obj = "wall"
    elif score > 20000:
        obj = "car"
    elif:
        obj = "person"
    elif
        obj = "pithole"
    elif
        obj = "stairs"
    else:
        obj = "obsatcle"

    return f"{obj} detected {direction} at {distance} cm"

if __name__ == "__main__":
    app.run()
