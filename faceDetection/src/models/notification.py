from datetime import datetime, date
from src.utils.extensions import db

class Notification(db.Model):
    __tablename__ = "notification"
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now().astimezone())
