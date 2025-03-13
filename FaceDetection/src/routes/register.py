import os
import csv
from flask import Blueprint, request, jsonify
from src.services.face_capture import capture_face
from config.config import CSV_FILE

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register_user():
    """Registers a new user by capturing their face and saving details in CSV."""
    data = request.json
    user_id = data.get("user_id")
    name = data.get("name")
    email = data.get("email")

    if not all([user_id, name, email]):
        return jsonify({"error": "Missing required fields"}), 400

    image_dir = capture_face(name)
    
    if not image_dir:
        return jsonify({"error": "Face capture failed. Try again."}), 500

    image_path = os.path.join(image_dir, "0.jpg")  
    
    # Save user details in CSV
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([user_id, name, email, image_path])

    return jsonify({"message": "User registered successfully", "image_path": image_path}), 201
