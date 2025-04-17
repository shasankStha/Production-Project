from datetime import datetime
from src.models.attendance import Attendance
from src.models.attendance_summary import AttendanceSummary
from src.models.user import User
from src.services.send_email import send_attendance_email
from src.utils.extensions import thread_pool
from flask import current_app


def insert_attendance(username, summary_id,db):
    try:
        # print("[INFO] Attendance started!!!")
        user = db.session.query(User).filter_by(username=username).first()
        if not user:
            raise ValueError(f"User with username {username} not found.")
        
        if user.status != 1:
            return True
                
        user_id = user.user_id
        existing_attendance = db.session.query(Attendance).filter_by(user_id=user_id, summary_id=summary_id).first()

        if existing_attendance:
            # print(f"Attendance already recorded for user '{username}' in summary {summary_id}.")
            return True

        attendance_time = datetime.now().astimezone()
        attendance = Attendance(
            user_id=user_id,
            summary_id=summary_id,
            timestamp=attendance_time
        )
        db.session.add(attendance)
        db.session.commit()

        summary = db.session.query(AttendanceSummary).filter_by(summary_id=summary_id).first()
        count = db.session.query(Attendance).filter_by(summary_id=summary_id).count()
        if summary:
            summary.present_count = count
            db.session.commit()

        def threaded_email_sender(app, user_email, first_name, attendance_time, user_id):
            with app.app_context():
                send_attendance_email(app, user_email, first_name, attendance_time, user_id)

        thread_pool.submit(threaded_email_sender, current_app._get_current_object(), user.email, user.first_name, attendance_time, user_id)



        return True
    except Exception as e:
        print(f"Error inserting attendance: {str(e)}")
        db.session.rollback()
        return False


def get_or_create_attendance_summary(db):
    today = datetime.today().date()

    summary = db.session.query(AttendanceSummary).filter_by(attendance_date=today).first()
    if not summary:
        summary = AttendanceSummary(attendance_date=today)
        db.session.add(summary)
        db.session.commit()

    return summary