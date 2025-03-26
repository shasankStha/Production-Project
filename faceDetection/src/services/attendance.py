from datetime import datetime
from src.models.attendance import Attendance
from src.models.attendance_summary import AttendanceSummary
from src.models.user import User

def insert_attendance(username, summary_id,db):
    try:
        user = db.session.query(User).filter_by(username=username).first()
        if not user:
            raise ValueError(f"User with username {username} not found.")
                
        user_id = user.user_id
        existing_attendance = db.session.query(Attendance).filter_by(user_id=user_id, summary_id=summary_id).first()

        if existing_attendance:
            print(f"Attendance already recorded for user '{username}' in summary {summary_id}.")
            return True

        attendance = Attendance(
            user_id=user_id,
            summary_id=summary_id,
            timestamp=datetime.utcnow()
        )
        db.session.add(attendance)
        db.session.commit()

        summary = db.session.query(AttendanceSummary).filter_by(summary_id=summary_id).first()
        if summary:
            summary.present_count += 1
            db.session.commit()

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