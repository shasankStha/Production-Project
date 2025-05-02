from src.utils.extensions import mail, db
from flask_mail import Message
from src.models.notification import Notification

def send_attendance_email(current_app, user_email, first_name, attendance_time,user_id):
    """Function to send an email notification"""
    try:
        subject = "Attendance Confirmation"
        body = f"Hello {first_name},\n\nYour attendance has been recorded successfully on {attendance_time.strftime('%Y-%m-%d')} at {attendance_time.strftime('%H:%M:%S')}.\n\nThank you!\n\nBest Regards,\nFacial Attendance System"

        html_body = f"""
                        <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    background-color: #f3f4f6;
                                    margin: 0;
                                    padding: 20px;
                                }}
                                .email-container {{
                                    max-width: 600px;
                                    background-color: #f3f4f6;
                                    margin: auto;
                                    border-radius: 8px;
                                    overflow: hidden;
                                    box-shadow: 0 0 10px rgba(0,0,0,0.05);
                                }}
                                .header {{
                                    background-color: #22c55e;  
                                    color: white;
                                    padding: 30px 20px;
                                    text-align: center;
                                }}
                                .header-icon {{
                                    font-size: 40px;
                                    margin-bottom: 10px;
                                }}
                                .content {{
                                    padding: 30px 20px;
                                    text-align: center;
                                }}
                                .content h1 {{
                                    color: #111827;
                                    font-size: 22px;
                                }}
                                .content p {{
                                    color: #4b5563;
                                    font-size: 16px;
                                    margin: 20px 0;
                                }}
                                .footer {{
                                    background-color: #f9fafb;
                                    padding: 20px;
                                    text-align: center;
                                    font-size: 13px;
                                    color: #9ca3af;
                                }}
                                .footer a {{
                                    color: #6b7280;
                                    text-decoration: none;
                                    margin: 0 5px;
                                }}
                                .button {{
                                    display: inline-block;
                                    background-color: #ef4444;
                                    color: white;
                                    padding: 10px 20px;
                                    margin-top: 20px;
                                    border-radius: 6px;
                                    text-decoration: none;
                                    font-size: 16px;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="email-container">
                                <div class="header">
                                    <div class="header-icon">📧</div>
                                    <h2>Attendance Confirmation</h2>
                                </div>
                                <div class="content">
                                    <h1>Hello {first_name},</h1>
                                    <p>Your attendance has been successfully marked on <strong>{attendance_time.strftime('%Y-%m-%d')}</strong> at <strong>{attendance_time.strftime('%H:%M:%S')}</strong>.</p>
                                    <p>Thank you for your presence.</p>
                                    <!-- Optional: Add a button if needed -->
                                    <!-- <a href="#" class="button">View Attendance</a> -->
                                </div>
                                <div class="footer">
                                    <p>Thapathali, Kathmandu</p>
                                    <p><a href="#">Privacy Policy</a> | <a href="#">Contact</a></p>
                                </div>
                            </div>
                        </body>
                        </html>
                        """
        
        with current_app.app_context():
            msg = Message(subject, recipients=[user_email], body=body, html = html_body)
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