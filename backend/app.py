from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import os
import face_recognition

app = Flask(__name__)
CORS(app)  # Enable frontend-backend communication

DATASET_PATH = "dataset/"

# Ensure dataset folder exists
if not os.path.exists(DATASET_PATH):
    os.makedirs(DATASET_PATH)

@app.route('/register', methods=['POST'])
def register_face():
    """Registers a new user by saving their face image."""
    user_id = request.form.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # Save uploaded image
    file = request.files["image"]
    user_folder = os.path.join(DATASET_PATH, user_id)
    os.makedirs(user_folder, exist_ok=True)
    
    file_path = os.path.join(user_folder, "face.jpg")
    file.save(file_path)

    return jsonify({"message": f"Face registered successfully for {user_id}"}), 200

@app.route('/recognize', methods=['POST'])
def recognize_face():
    """Recognizes a face from an uploaded image."""
    file = request.files["image"]
    file_path = "temp.jpg"
    file.save(file_path)

    # Load uploaded image
    unknown_img = face_recognition.load_image_file(file_path)
    unknown_encodings = face_recognition.face_encodings(unknown_img)

    if len(unknown_encodings) == 0:
        return jsonify({"error": "No face detected"}), 400

    unknown_encoding = unknown_encodings[0]

    # Compare with registered users
    for user_id in os.listdir(DATASET_PATH):
        user_img_path = os.path.join(DATASET_PATH, user_id, "face.jpg")
        if os.path.exists(user_img_path):
            registered_img = face_recognition.load_image_file(user_img_path)
            registered_encoding = face_recognition.face_encodings(registered_img)[0]
            
            result = face_recognition.compare_faces([registered_encoding], unknown_encoding)
            if result[0]:  # Match found
                return jsonify({"message": f"Access Granted: {user_id}"}), 200

    return jsonify({"message": "Access Denied"}), 403

if __name__ == '__main__':
    app.run(debug=True)
