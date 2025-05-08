from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from src.models.user import User
from src.utils.extensions import db,mail
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_mail import Message

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email, status = 1).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.user_id), additional_claims={"role": user.role})
        return jsonify({"access_token": access_token, "role": user.role}), 200
    
    return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route("/change_password", methods=["PUT"])
@jwt_required()
def change_password():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        data = request.get_json()
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        if not current_password or not new_password:
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        if not user.check_password(current_password):
            return jsonify({"success": False, "message": "Current password is incorrect"}), 401

        user.set_password(new_password)
        db.session.commit()

        return jsonify({"success": True, "message": "Password changed successfully"}), 200

    except Exception as e:
        print(f"[ERROR] Changing password: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@auth_bp.route("/forgot_password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")
    user = User.query.filter_by(email=email).first()

    if user:
        token = user.generate_reset_token()
        reset_link = f"http://localhost:3000/reset-password/{token}"

        # Send email
        msg = Message("Reset Your Password",
                      recipients=[email],
                      body=f"Click the link to reset your password: {reset_link}")
        mail.send(msg)

    # Always return this message to prevent revealing user existence
    return jsonify({"message": "Reset link was sent to the email address"}), 200




@auth_bp.route("/reset_password/<token>", methods=["POST"])
def reset_password(token):
    data = request.get_json()
    new_password = data.get("new_password")

    user = User.verify_reset_token(token)
    if not user:
        return jsonify({"success": False, "message": "Invalid or expired token"}), 400

    user.set_password(new_password)
    db.session.commit()
    return jsonify({"success": True, "message": "Password reset successful"}), 200