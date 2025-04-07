from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User
from src.models.attendance import Attendance
from src.models.attendance_summary import AttendanceSummary
from src.utils.extensions import db
from src.services.ipfs_store import store_attendance_ipfs
from src.utils.retrieve_attendance_blockchain import retrieve_attendance_summary_and_data
import json

admin_bp = Blueprint("admin", __name__)

# @admin_bp.route("/register", methods=["POST"])
# @jwt_required()
# def is_admin():
#     current_user = get_jwt_identity()
#     if current_user["role"] != "admin":
#         return jsonify({"message": "Access denied"}), 403

#     data = request.get_json()
#     new_user = User(
#         username=data["username"],
#         email=data["email"],
#         role=data.get("role", "user")
#     )
#     new_user.set_password(data["password"])
    
#     db.session.add(new_user)
#     db.session.commit()
    
#     return jsonify({"message": "User registered successfully"}), 201


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
        
        grouped_attendance = {}


        for record in records:
            attendance_date = record.attendance_date.strftime("%Y-%m-%d")
            user_data = {
                "attendance_id": record.attendance_id,
                "username": record.username,
                "name": f"{record.first_name} {record.last_name}",
                "time": record.timestamp.strftime("%H:%M:%S"),
            }

            # Add user_data under the corresponding attendance_date key
            if attendance_date not in grouped_attendance:
                grouped_attendance[attendance_date] = []
            
            grouped_attendance[attendance_date].append(user_data)

        return jsonify({"success": True, "attendance_records": grouped_attendance})
    except Exception as e:
        print(f"[ERROR] Failed to fetch attendance records: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@admin_bp.route("/store_attendance", methods=["POST"])
@jwt_required()
def store_attendance():
    """
    Trigger storing attendance records for a given date in IPFS and Blockchain.
    """
    try:
        current_user = get_jwt_identity()
        if current_user["role"] != "admin":
            return jsonify({"message": "Access denied"}), 403

        data = request.get_json()
        date_str = data.get("date")
        if not date_str:
            return jsonify({"success": False, "message": "Date parameter is required"}), 400

        # Call the function to store attendance
        tx_receipt = store_attendance_ipfs(date_str)
        if tx_receipt:
            return jsonify({"success": False, "message": "Failed to store attendance"}), 500

        return jsonify({
            "success": True,
            "message": "Attendance stored successfully",
            "tx_receipt": tx_receipt
        }), 200

    except Exception as e:
        print(f"[ERROR] Failed to store attendance: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    

@admin_bp.route("/attendance_summary", methods=["GET"])
def get_attendance_summary():
    try:
        attendance_summary = db.session.query(AttendanceSummary.attendance_date).all()

        summary_data = [record.attendance_date.strftime("%Y-%m-%d") for record in attendance_summary]
        
        return jsonify({"success": True, "attendance_summary": summary_data})
    except Exception as e:
        print(f"[ERROR] Failed to fetch attendance summary: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@admin_bp.route("/attendance_records/<attendance_date>", methods=["GET"])
def get_attendance_records_by_date(attendance_date):
    try:
        attendance_data = retrieve_attendance_summary_and_data(attendance_date)
        if "error" in attendance_data or not attendance_data:
            return jsonify({"success": False, "error": attendance_data["error"]}), 500
        
        
        ipfs_data = json.loads(attendance_data["ipfs_data"])
        attendance_records = ipfs_data["attendance_records"]

        if not attendance_records:
            return jsonify({"success": False, "error": "No attendance records found."}), 404


        records = []
        for record in attendance_records:
            user = User.query.get(record["user_id"])
            if user:
                records.append({
                    "attendance_id": record["attendance_id"],
                    "user_id": record["user_id"],
                    "username": user.username,
                    "name": f"{user.first_name} {user.last_name}",
                    "time": record["timestamp"]
                })

        return jsonify({"success": True, "attendance_records": records})

    
    except Exception as e:
        print(f"[ERROR] Failed to fetch attendance records for date {attendance_date}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500