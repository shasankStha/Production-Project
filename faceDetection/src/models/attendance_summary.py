from datetime import datetime, date
from src.utils.extensions import db
from src.models.blockchain_record import BlockchainRecord

class AttendanceSummary(db.Model):
    __tablename__ = "attendance_summary"
    summary_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attendance_date = db.Column(db.Date, nullable=False, default=date.today)
    ipfs_cid = db.Column(db.String, nullable=True)
    present_count = db.Column(db.Integer, nullable=False, default=0)
    
    attendance_records = db.relationship('Attendance', backref='attendance_summary', lazy=True)
    blockchain_records = db.relationship('BlockchainRecord', backref='attendance_summary', lazy=True)