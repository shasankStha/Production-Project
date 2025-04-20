import os
import secrets
import string
from flask import Blueprint, request, jsonify
from src.services.face_capture import capture_face
from src.utils.extensions import db, socketio,mail
from src.utils.train_model import train_model
from src.models.user import User
from sqlalchemy import func
from flask_mail import Message

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        username = data.get("username")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")

        # Check for missing required fields
        if not all([username, first_name, last_name, email]):
            socketio.emit("registration_status", {"error": "Missing required fields"})
            return jsonify({"error": "Missing required fields"}), 400


        username = username.lower()
        email = email.lower()

        existing_user = User.query.filter(
            (func.lower(User.username) == username) | (func.lower(User.email) == email)
        ).first()

        if existing_user:
            socketio.emit("registration_status", {"error": "Username or email already exists"})
            return jsonify({"error": "Username or email already exists"}), 409
        
        socketio.emit("registration_status", {"message": "Registration started..."})

        face_identifier = f"{username}.{first_name} {last_name}"
        image_dir = capture_face(face_identifier)

        if not image_dir:
            socketio.emit("registration_status", {"error": "Face capture failed. Try again."})
            return jsonify({"error": "Face capture failed. Try again."}), 500
        
        socketio.emit("registration_status", {"message": "Face capture completed"})
        image_path = os.path.join(image_dir, "0.jpg")

        # Generate random password
        temp_password = generate_random_password()

        # Create the new user record
        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role="user"
        )
        new_user.set_password(temp_password)
        db.session.add(new_user)
        db.session.commit()

        if not train_model(face_identifier, image_dir):
            db.session.delete(new_user)
            db.session.commit()
            socketio.emit("registration_status", {"error": "Model training failed."})
            return jsonify({"error": "Model training failed."}), 500
        
        token = new_user.generate_reset_token()
        reset_link = f"http://localhost:3000/reset-password/{token}"

        msg = Message(
            subject="Set Your Password",
            recipients=[email],
            body=f"Hi {first_name},\n\nYour account has been created. Click the link below to set your password:\n{reset_link}\n\nThank you!"
        )
        mail.send(msg)

        socketio.emit("registration_status", {"message": "User registered successfully!"})
        return jsonify({"message": "User registered successfully", "image_path": image_path}), 201

    except Exception as e:
        socketio.emit("registration_status", {"error": f"An unexpected error occurred: {str(e)}"})
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    
def generate_random_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))
