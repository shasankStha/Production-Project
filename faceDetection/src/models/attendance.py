from datetime import datetime, date
from src.utils.extensions import db
from src.models.attendance_summary import AttendanceSummary

class Attendance(db.Model):
    __tablename__ = "attendance"
    attendance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    summary_id = db.Column(db.Integer, db.ForeignKey('attendance_summary.summary_id'), nullable=False)