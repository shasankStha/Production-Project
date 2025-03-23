from datetime import datetime, date
from src.utils.extensions import db

class BlockchainRecord(db.Model):
    __tablename__ = "blockchain_record"
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    summary_id = db.Column(db.Integer, db.ForeignKey('attendance_summary.summary_id'), nullable=False)
    transaction_hash = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)