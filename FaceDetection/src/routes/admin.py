from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User
from src.utils.extensions import db

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/register", methods=["POST"])
@jwt_required()
def register_user():
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    data = request.get_json()
    new_user = User(
        username=data["username"],
        email=data["email"],
        role=data.get("role", "user")
    )
    new_user.set_password(data["password"])
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201
