from flask import Blueprint, jsonify, make_response, request
from src.models.attendance_summary import AttendanceSummary
from src.models.attendance import Attendance
from src.models.blockchain_record import BlockchainRecord
from src.blockchain.get_cid_from_blockchain import get_attendance
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.ipfs_store import ipfs_get_data
from src.models.user import User
import json
from datetime import datetime, date
from src.utils.extensions import db

user_bp = Blueprint("user", __name__)

@user_bp.route("/attendance_dates", methods=["GET"])
@jwt_required()
def get_user_attendance_dates():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404

        blockchain_record = BlockchainRecord.query.all()
        attended_dates = []
        total_attendance_days = len(blockchain_record)

        for row in blockchain_record:
            if row.blockchain_record_id:
                record = get_attendance(row.blockchain_record_id)
                attendance_data = json.loads(ipfs_get_data(record.get("cid")))
                if "attendance_records" in attendance_data:
                    for rec in attendance_data["attendance_records"]:
                        if int(rec["user_id"]) == int(user_id):
                            attended_dates.append(str(attendance_data.get("date")))
                            break

        today_str = date.today().isoformat()
        source = "blockchain"
        disclaimer = None

        if today_str not in attended_dates:
            today_attendance = (
                db.session.query(Attendance)
                .join(AttendanceSummary, Attendance.summary_id == AttendanceSummary.summary_id)
                .filter(
                    Attendance.user_id == user_id,
                    AttendanceSummary.attendance_date == date.today()
                )
                .first()
            )

            if today_attendance:
                total_attendance_days+=1
                attended_dates.append(today_str)
                source = "postgres"
                disclaimer = "Today's attendance data is from Postgres and not yet recorded on the blockchain."

        response = make_response(jsonify({
            "success": True,
            "total_attendance_days": total_attendance_days,
            "attendance_dates": list(attended_dates),
            "source": source,
            "disclaimer": disclaimer
        }))
        response.headers["Cache-Control"] = "public, max-age=300"
        return response

    except Exception as e:
        print(f"[ERROR] Fetching attendance dates for user: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
