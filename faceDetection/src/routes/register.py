import os
import csv
from flask import Blueprint, request, jsonify
from src.services.face_capture import capture_face
from config.config import CSV_FILE, IMAGE_DIR
from src.utils.extensions import socketio
from src.utils.train_model import train_model

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        user_id = data.get("user_id")
        name = data.get("name")
        email = data.get("email")

        if not all([user_id, name, email]):
            socketio.emit("registration_status", {"error": "Missing required fields"})
            return jsonify({"error": "Missing required fields"}), 400

        socketio.emit("registration_status", {"message": "Registration started..."})

        image_dir = capture_face(user_id+"."+name)
        if not image_dir:
            socketio.emit("registration_status", {"error": "Face capture failed. Try again."})
            return jsonify({"error": "Face capture failed. Try again."}), 500

        user_identifier = f"{user_id}) {name}"
        image_path = os.path.join(image_dir, "0.jpg")

        socketio.emit("registration_status", {"message": "Face capture completed"})

        try:
            with open(CSV_FILE, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([user_id, name, email, image_path])
        except Exception as e:
            socketio.emit("registration_status", {"error": f"Failed to save user details: {str(e)}"})
            return jsonify({"error": f"Failed to save user details: {str(e)}"}), 500

        if not train_model(name, image_dir):
            return jsonify({"error": "Model training failed."}), 500
        
        socketio.emit("registration_status", {"message": "User registered successfully!"})
        return jsonify({"message": "User registered successfully", "image_path": image_path}), 201

    except Exception as e:
        socketio.emit("registration_status", {"error": f"An unexpected error occurred: {str(e)}"})
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500