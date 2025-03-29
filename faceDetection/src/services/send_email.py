from src.utils.extensions import mail, db
from flask import current_app
from flask_mail import Message
from src.models.notification import Notification

def send_attendance_email(user_email, first_name, attendance_time,user_id):
    """Function to send an email notification"""
    try:
        subject = "Attendance Confirmation"
        body = f"Hello {first_name},\n\nYour attendance has been recorded successfully on {attendance_time.strftime('%Y-%m-%d')} at {attendance_time.strftime('%H:%M:%S')}.\n\nThank you!\n\nBest Regards,\nFacial Attendance System"

        msg = Message(subject, recipients=[user_email], body=body)
        
        with current_app.app_context():
            mail.send(msg)

        notification = Notification(
            user_id=user_id,
            timestamp=attendance_time
        )
        db.session.add(notification)
        db.session.commit()
        
        print(f"[INFO] Email sent successfully to {user_email}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {str(e)}")