from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User
from src.models.attendance import Attendance
from src.models.attendance_summary import AttendanceSummary
from src.utils.extensions import db

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/register", methods=["POST"])
@jwt_required()
def is_admin():
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


@admin_bp.route("/attendance_records", methods=["GET"])
def get_attendance_records():
    try:
        records = db.session.query(
            Attendance.attendance_id,
            User.username,
            User.first_name,
            User.last_name,
            Attendance.timestamp,
            AttendanceSummary.attendance_date
        ).join(User, Attendance.user_id == User.user_id)\
         .join(AttendanceSummary, Attendance.summary_id == AttendanceSummary.summary_id)\
         .order_by(Attendance.timestamp.desc()).all()

        attendance_data = [
            {
                "attendance_id": record.attendance_id,
                "username": record.username,
                "name": f"{record.first_name} {record.last_name}",
                "date": record.attendance_date.strftime("%Y-%m-%d"),
                "time": record.timestamp.strftime("%H:%M:%S"),
            }
            for record in records
        ]

        return jsonify({"success": True, "attendance_records": attendance_data})
    except Exception as e:
        print(f"[ERROR] Failed to fetch attendance records: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
