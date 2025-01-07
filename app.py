import os
import json
import cv2
import numpy as np
from flask import Flask, request, jsonify
import base64

# Initialize Flask app
app = Flask(__name__)

# Path to the data file
data_file = "face_db.json"

# In-memory database
face_db = []

# Load data from file if it exists
def load_data():
    global face_db
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            face_db = json.load(f)

# Save data to file
def save_data():
    with open(data_file, "w") as f:
        json.dump(face_db, f, indent=4)

# Process image to generate descriptors
def generate_descriptors(image_data):
    try:
        # Decode the base64 image data
        image_bytes = base64.b64decode(image_data)
        np_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("Invalid image data")

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Resize the image to a fixed size (e.g., 100x100)
        resized_image = cv2.resize(gray_image, (100, 100))

        # Flatten the image to create a simple descriptor (example: mean pixel values)
        descriptors = resized_image.flatten().tolist()
        return descriptors
    except Exception as e:
        raise ValueError(f"Error processing image: {e}")

# Endpoint to get all faceDb entries
@app.route("/faceDb", methods=["GET"])
def get_faces():
    return jsonify(face_db), 200

# Endpoint to add a new faceDb entry
@app.route("/faceDb", methods=["POST"])
def add_face():
    data = request.get_json()

    # Validate input
    if not data or "label" not in data or "thumbnail" not in data:
        return jsonify({"error": "Missing required fields: label, thumbnail"}), 400

    try:
        # Generate descriptors from the thumbnail image
        descriptors = generate_descriptors(data["thumbnail"])

        # Add the new entry
        face_db.append({
            "label": data["label"],
            "thumbnail": data["thumbnail"],
            "descriptors": descriptors,
        })

        # Save to disk
        save_data()
        return jsonify({"message": "Entry added successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Load data on startup
if __name__ == "__main__":
    load_data()
    app.run(debug=True)
