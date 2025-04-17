from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User
from sqlalchemy import func, or_
from src.models.attendance import Attendance
from src.models.attendance_summary import AttendanceSummary
from src.utils.extensions import db
from src.services.ipfs_store import store_attendance_ipfs
from src.utils.retrieve_attendance_blockchain import retrieve_attendance_summary_and_data
import json
from datetime import date, datetime,timedelta
from collections import defaultdict


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


# @admin_bp.route("/attendance_records", methods=["GET"])
# def get_attendance_records():
#     try:
        # records = db.session.query(
        #     Attendance.attendance_id,
        #     User.username,
        #     User.first_name,
        #     User.last_name,
        #     Attendance.timestamp,
        #     AttendanceSummary.attendance_date
        # ).join(User, Attendance.user_id == User.user_id)\
        #  .join(AttendanceSummary, Attendance.summary_id == AttendanceSummary.summary_id)\
        #  .order_by(Attendance.timestamp.desc()).all()
        
#         grouped_attendance = {}


#         for record in records:
#             attendance_date = record.attendance_date.strftime("%Y-%m-%d")
#             user_data = {
#                 "attendance_id": record.attendance_id,
#                 "username": record.username,
#                 "name": f"{record.first_name} {record.last_name}",
#                 "time": record.timestamp.strftime("%H:%M:%S"),
#             }

#             # Add user_data under the corresponding attendance_date key
#             if attendance_date not in grouped_attendance:
#                 grouped_attendance[attendance_date] = []
            
#             grouped_attendance[attendance_date].append(user_data)

#         return jsonify({"success": True, "attendance_records": grouped_attendance})
#     except Exception as e:
#         print(f"[ERROR] Failed to fetch attendance records: {str(e)}")
#         return jsonify({"success": False, "error": str(e)}), 500

@admin_bp.route("/store_attendance", methods=["POST"])
@jwt_required()
def store_attendance():
    """
    Trigger storing attendance records for a given date in IPFS and Blockchain.
    """
    try:
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
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

        response = make_response(jsonify({
            "success": True,
            "message": "Attendance stored successfully",
            "tx_receipt": tx_receipt
        }), 200)
        response.headers["Cache-Control"] = "public, max-age=300"
        return response

    except Exception as e:
        print(f"[ERROR] Failed to store attendance: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    

@admin_bp.route("/attendance_summary", methods=["GET"])
def get_attendance_summary():
    try:
        attendance_summary = db.session.query(AttendanceSummary.attendance_date).all()

        summary_data = [record.attendance_date.strftime("%Y-%m-%d") for record in attendance_summary]
        
        response = make_response(jsonify({"success": True, "attendance_summary": summary_data}))
        response.headers["Cache-Control"] = "public, max-age=300"
        return response
    except Exception as e:
        print(f"[ERROR] Failed to fetch attendance summary: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@admin_bp.route("/attendance_records/<attendance_date>", methods=["GET"])
def get_attendance_records_by_date(attendance_date):
    try:
        attendance_data = retrieve_attendance_summary_and_data(attendance_date)
    
        if "error" in attendance_data or not attendance_data:
            if attendance_date == date.today().isoformat():
                print("[INFO] Blockchain data unavailable for today. Falling back to Postgres.")
                return fetch_from_postgres(attendance_date)
            else:
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
    
def fetch_from_postgres(attendance_date):
    try:
        start_datetime = datetime.strptime(attendance_date, "%Y-%m-%d")

        attendance_records = db.session.query(
            Attendance.attendance_id,
            User.user_id,
            User.username,
            User.first_name,
            User.last_name,
            Attendance.timestamp,
            AttendanceSummary.attendance_date
        ).join(User, Attendance.user_id == User.user_id)\
         .join(AttendanceSummary, Attendance.summary_id == AttendanceSummary.summary_id)\
         .filter(AttendanceSummary.attendance_date == start_datetime.date())\
         .order_by(Attendance.timestamp.desc()).all()
        
        if not attendance_records:
            return jsonify({"success": False, "error": "No attendance records found in Postgres."}), 404

        records = []
        for record in attendance_records:
            records.append({
                "attendance_id": record.attendance_id,
                "user_id": record.user_id,
                "username": record.username,
                "name": f"{record.first_name} {record.last_name}",
                "time": record.timestamp.isoformat()
            })

        response = make_response(jsonify({
            "success": True,
            "attendance_records": records,
            "source": "postgres",
            "disclaimer": "Data is fetched from Postgres as today's blockchain record is not yet available."
        }))
        response.headers["Cache-Control"] = "public, max-age=300"
        return response

    except Exception as e:
        print(f"[ERROR] Postgres fallback failed: {str(e)}")
        return jsonify({"success": False, "error": "Failed to fetch from Postgres."}), 500
    
def fetch_analytics_from_postgres(date_str):
    """Helper function to fetch attendance count for a given date using Postgres."""
    dt = datetime.strptime(date_str, "%Y-%m-%d").date()
    total = db.session.query(func.count(Attendance.attendance_id)) \
                .join(AttendanceSummary, Attendance.summary_id == AttendanceSummary.summary_id) \
                .filter(AttendanceSummary.attendance_date == dt).scalar()
    return total

@admin_bp.route("/analytics/attendance", methods=["GET"])
def get_attendance_analytics():
    """
    Returns aggregated attendance data (total attendance per day) for a given date range.
    Uses blockchain data when available and for today's date falls back to Postgres if needed.
    """
    try:
        start_date_str = request.args.get("start_date")
        end_date_str = request.args.get("end_date")
        if not start_date_str or not end_date_str:
            return jsonify({"success": False, "error": "start_date and end_date are required"}), 400

        start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        analytics = []
        current_date = start_date_obj
        while current_date <= end_date_obj:
            date_str = current_date.isoformat()
            # Attempt to fetch blockchain data for the day
            attendance_data = retrieve_attendance_summary_and_data(date_str)
            total_attendance = 0
            used_source = "blockchain"
            disclaimer = None

            if "error" in attendance_data or not attendance_data:
                if date_str == date.today().isoformat():
                    # Fallback for current day using Postgres
                    total_attendance = fetch_analytics_from_postgres(date_str)
                    used_source = "postgres"
                    disclaimer = "Data is fetched from Postgres as today's blockchain record is not yet available."
                else:
                    total_attendance = 0
            else:
                ipfs_data = json.loads(attendance_data["ipfs_data"])
                attendance_records = ipfs_data.get("attendance_records", [])
                total_attendance = len(attendance_records)

            analytics.append({
                "date": date_str,
                "total_attendance": total_attendance,
                "source": used_source,
                "disclaimer": disclaimer
            })
            current_date += timedelta(days=1)

            response = make_response(jsonify({
            "success": True,
            "analytics": analytics
        }))

        response.headers["Cache-Control"] = "public, max-age=300"
        return response
    except Exception as e:
        print(f"[ERROR] Fetching analytics: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


def search_postgres_attendance(date_str, query_text):
    """Helper function to search Postgres attendance records for a given date and query."""
    dt = datetime.strptime(date_str, "%Y-%m-%d").date()
    query_obj = db.session.query(
            Attendance.attendance_id,
            User.user_id,
            User.username,
            User.first_name,
            User.last_name,
            Attendance.timestamp,
            AttendanceSummary.attendance_date
        ).join(User, Attendance.user_id == User.user_id)\
         .join(AttendanceSummary, Attendance.summary_id == AttendanceSummary.summary_id)\
         .filter(AttendanceSummary.attendance_date == dt)
    if query_text:
        query_obj = query_obj.filter(
            or_(
                User.username.ilike(f"%{query_text}%"),
                User.first_name.ilike(f"%{query_text}%"),
                User.last_name.ilike(f"%{query_text}%")
            )
        )
    results = query_obj.order_by(Attendance.timestamp.desc()).all()
    records = []
    for r in results:
        records.append({
            "attendance_id": r.attendance_id,
            "user_id": r.user_id,
            "username": r.username,
            "name": f"{r.first_name} {r.last_name}",
            "time": r.timestamp.isoformat()
        })
    return records


@admin_bp.route("/search_attendance", methods=["GET"])
def search_attendance():
    """
    Advanced Filtering & Search Endpoint.
    For each date in the provided range, uses blockchain records for that day.
    For the current day, if blockchain records are unavailable, falls back to Postgres.
    Also filters results by a free-text query on username, first name, or last name.
    """
    try:
        query_text = request.args.get("query", "")
        start_date_str = request.args.get("start_date")
        end_date_str = request.args.get("end_date")
        if not start_date_str or not end_date_str:
            return jsonify({"success": False, "error": "start_date and end_date are required"}), 400

        start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        results = []
        current_date = start_date_obj
        while current_date <= end_date_obj:
            date_str = current_date.isoformat()
            attendance_data = retrieve_attendance_summary_and_data(date_str)
            records = []
            if "error" in attendance_data or not attendance_data:
                if date_str == date.today().isoformat():
                    records = search_postgres_attendance(date_str, query_text)
                else:
                    records = []
            else:
                ipfs_data = json.loads(attendance_data["ipfs_data"])
                records = ipfs_data.get("attendance_records", [])
                # In-memory filtering based on query_text
                filtered = []
                for rec in records:
                    user = User.query.get(rec["user_id"])
                    if user:
                        combined = (user.username + " " + user.first_name + " " + user.last_name).lower()
                        if query_text.lower() in combined:
                            filtered.append({
                                "attendance_id": rec["attendance_id"],
                                "user_id": rec["user_id"],
                                "username": user.username,
                                "name": f"{user.first_name} {user.last_name}",
                                "time": rec["timestamp"]
                            })
                records = filtered

            results.extend(records)
            current_date += timedelta(days=1)
        
        return jsonify({"success": True, "attendance_records": results})
    except Exception as e:
        print(f"[ERROR] Search attendance: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    
@admin_bp.route("/top_attendees", methods=["GET"])
def get_top_attendees():
    """
    Returns the top 5 users with the highest total attendance (based on blockchain data).
    Response is cacheable for 5 minutes.
    """
    try:
        attendance_summary = db.session.query(AttendanceSummary.attendance_date).all()
        user_attendance_count = defaultdict(int)

        for record in attendance_summary:
            date_str = record.attendance_date.strftime("%Y-%m-%d")
            attendance_data = retrieve_attendance_summary_and_data(date_str)

            if "error" in attendance_data or not attendance_data:
                continue

            ipfs_data = json.loads(attendance_data["ipfs_data"])
            attendance_records = ipfs_data.get("attendance_records", [])

            for rec in attendance_records:
                user_attendance_count[rec["user_id"]] += 1

        # Get top 5 users sorted by count descending
        top_5 = sorted(user_attendance_count.items(), key=lambda x: x[1], reverse=True)[:5]
        result = []

        for user_id, count in top_5:
            user = User.query.get(user_id)
            if user:
                result.append({
                    "user_id": user.user_id,
                    "username": user.username,
                    "name": f"{user.first_name} {user.last_name}",
                    "total_attendance": count
                })

        response = make_response(jsonify({"success": True, "top_attendees": result}))
        response.headers["Cache-Control"] = "public, max-age=300"
        return response

    except Exception as e:
        print(f"[ERROR] Fetching top attendees from blockchain: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    
@admin_bp.route("/attendance_by_day_of_week", methods=["GET"])
def get_attendance_by_day_of_week():
    try:
        # Get the attendance data for the given date range from blockchain
        start_date_str = request.args.get("start_date")
        end_date_str = request.args.get("end_date")
        if not start_date_str or not end_date_str:
            return jsonify({"success": False, "error": "start_date and end_date are required"}), 400

        start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        # Initialize dictionary to store attendance counts per day of the week
        attendance_by_day = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}  # Monday to Sunday

        current_date = start_date_obj
        while current_date <= end_date_obj:
            date_str = current_date.isoformat()
            attendance_data = retrieve_attendance_summary_and_data(date_str)

            if "error" in attendance_data or not attendance_data:
                current_date += timedelta(days=1)
                continue  # Skip this day if no data is available

            ipfs_data = json.loads(attendance_data["ipfs_data"])
            attendance_records = ipfs_data.get("attendance_records", [])

            for record in attendance_records:
                # Get the day of the week (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
                timestamp = record["timestamp"]
                timestamp_date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
                day_of_week = timestamp_date.weekday()
                attendance_by_day[day_of_week] += 1

            current_date += timedelta(days=1)

        # Convert the day counts to a list of data for the frontend
        day_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        attendance_data_for_pie = {
            "labels": day_labels,
            "datasets": [{
                "data": list(attendance_by_day.values())
            }]
        }

    
        response = make_response(jsonify({"success": True, "attendance_by_day": attendance_data_for_pie}))
        response.headers["Cache-Control"] = "public, max-age=300"
        return response

    except Exception as e:
        print(f"[ERROR] Failed to fetch attendance by day of the week: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
