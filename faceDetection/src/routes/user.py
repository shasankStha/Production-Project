from flask import Blueprint, jsonify
from src.models.attendance_summary import AttendanceSummary
from src.models.blockchain_record import BlockchainRecord
from src.blockchain.get_cid_from_blockchain import get_attendance
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.ipfs_store import ipfs_get_data
from src.models.user import User
import json

user_bp = Blueprint("user", __name__)

@user_bp.route("/attendance_dates", methods=["GET"])
@jwt_required()
def get_user_attendance_dates():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404

        blockchain_record = BlockchainRecord.query.all()
        attended_dates = []

        for row in blockchain_record:
            if row.blockchain_record_id:
                record = get_attendance(row.blockchain_record_id)
                attendance_data = json.loads(ipfs_get_data(record.get("cid")))
                if "attendance_records" in attendance_data:
                    for rec in attendance_data["attendance_records"]:
                        if int(rec["user_id"]) == int(user_id):
                            attended_dates.append(str(attendance_data.get("date")))
                            break
        return jsonify({"success": True, "attendance_dates": attended_dates})

    except Exception as e:
        print(f"[ERROR] Fetching attendance dates for user: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
