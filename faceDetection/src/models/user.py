from src.utils.extensions import db, bcrypt
from src.models.notification import Notification
from src.models.attendance import Attendance

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, default=1)
    role = db.Column(db.String, nullable=False, default="user")

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    notifications = db.relationship('Notification', backref='user', lazy=True)
    attendance_records = db.relationship('Attendance', backref='user', lazy=True)