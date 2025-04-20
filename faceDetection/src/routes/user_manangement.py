from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User
from src.utils.extensions import db
from src.utils.train_model import remove_user_from_model, rename_user_in_model

user_management_bp = Blueprint("user_management", __name__)

@user_management_bp.route("/users", methods=["GET"])
@jwt_required()
def get_all_users():
    user_id = int(get_jwt_identity())
    current_user = User.query.get(user_id)
    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    users = User.query.filter(User.status == 1, User.role != "admin").all()
    result = []
    for user in users:
        result.append({
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        })

    return jsonify({"success": True, "users": result})

@user_management_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    admin_user_id = int(get_jwt_identity())
    current_user = User.query.get(admin_user_id)
    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403
    
    user = User.query.get(user_id)
    if not user or user.status == 0:
        return jsonify({"message": "User not found"}), 404
    
    old_email = user.email
    old_username = user.username
    remove_user_from_model(f"{user.username}.{user.first_name} {user.last_name}")

    user.status = 0
    user.email = str(user_id)+old_email
    user.username = str(user_id)+old_username
    db.session.commit()


    return jsonify({"success": True, "message": "User soft-deleted"})


@user_management_bp.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    admin_user_id = int(get_jwt_identity())
    current_user = User.query.get(admin_user_id)
    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.get_json()
    new_username = data.get("username")
    new_email = data.get("email")
    new_first_name = data.get("first_name")
    new_last_name = data.get("last_name")

    old_username = user.username
    old_first_name = user.first_name
    old_last_name = user.last_name

    if new_username != user.username:
        existing_user = User.query.filter(User.username == new_username, User.user_id != user.user_id).first()
        if existing_user:
            return jsonify({"message": "Username already taken"}), 400
        user.username = new_username

    if new_email != user.email:
        existing_email_user = User.query.filter(User.email == new_email, User.user_id != user.user_id).first()
        if existing_email_user:
            return jsonify({"message": "Email already taken"}), 400
        user.email = new_email

    if new_first_name:
        user.first_name = new_first_name

    if new_last_name:
        user.last_name = new_last_name


    new_label = f"{user.username}.{user.first_name} {user.last_name}"
    old_label = f"{old_username}.{old_first_name} {old_last_name}"
    if new_label != old_label:
        rename_user_in_model(old_label, new_label)

    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200