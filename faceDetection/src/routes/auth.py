from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from src.models.user import User
from src.utils.extensions import db,mail, thread_pool
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_mail import Message

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email, status = 1).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.user_id), additional_claims={"role": user.role})
        return jsonify({"access_token": access_token, "role": user.role}), 200
    
    return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route("/change_password", methods=["PUT"])
@jwt_required()
def change_password():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        data = request.get_json()
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        if not current_password or not new_password:
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        if not user.check_password(current_password):
            return jsonify({"success": False, "message": "Current password is incorrect"}), 401

        user.set_password(new_password)
        db.session.commit()

        return jsonify({"success": True, "message": "Password changed successfully"}), 200

    except Exception as e:
        print(f"[ERROR] Changing password: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@auth_bp.route("/forgot_password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")
    user = User.query.filter_by(email=email).first()

    if user:
        token = user.generate_reset_token()
        reset_link = f"http://localhost:3000/reset-password/{token}"

        msg_html = f"""
        <html>
        <head>
            <style>
                .container {{
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f9f9f9;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }}
                .button {{
                    background-color: #007bff;
                    color: white;
                    padding: 10px 15px;
                    text-decoration: none;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Password Reset Request</h2>
                <p>Click the button below to reset your password:</p>
                <p><a class="button" href="{reset_link}">Reset Password</a></p>
                <p>If you didn’t request this, you can safely ignore this email.</p>
            </div>
        </body>
        </html>
        """
        

        # Send email
        msg = Message("Reset Your Password",
                      recipients=[email],
                      body=f"Click the link to reset your password: {reset_link}",
                      html=htmlBodyCreator(reset_link))
        
        mail.send(msg)

    # Always return this message to prevent revealing user existence
    return jsonify({"message": "Reset link was sent to the email address"}), 200


def htmlBodyCreator(reset_link):
    return f"""
            <html>
                <head>
                    <style>
                        body {{
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                            background-color: #f4f4f4;
                            margin: 0;
                            padding: 0;
                            color: #333;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: 30px auto;
                            background-color: #ffffff;
                            border: 1px solid #e0e0e0;
                            border-radius: 8px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            padding: 30px;
                        }}
                        h2 {{
                            color: #007bff;
                            font-size: 24px;
                            margin-bottom: 20px;
                        }}
                        p {{
                            font-size: 16px;
                            line-height: 1.6;
                            margin: 10px 0;
                        }}
                        .button {{
                            background-color: #FFFFFF;
                            padding: 12px 20px;
                            text-decoration: none;
                            border: 1px solid #007bff;
                            font-size: 16px;
                            font-weight: bold;
                            border-radius: 6px;
                            display: inline-block;
                            margin-top: 20px;
                            transition: background-color 0.3s ease;
                        }}
                        .button:link,
                        .button:visited {{
                            color: red;
                            text-decoration: none;
                        }}
                        .button:hover {{
                            background-color: #0056b3;
                            color: white;
                        }}
                        .footer {{
                            font-size: 14px;
                            color: #888;
                            margin-top: 30px;
                            text-align: center;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2>Password Reset Request</h2>
                        <p>Dear User,</p>
                        <p>We received a request to reset your password. To proceed, click the button below:</p>
                        <p><a class="button" href="{reset_link}">Reset Password</a></p>
                        <p>If you did not request this, please disregard this email. Your account is safe.</p>
                        <p>Thank you,</p>
                        <p>Facial Recognition Attendance System</p>
                    </div>
                    <div class="footer">
                        <p>If you have any questions, feel free to contact our support team.</p>
                    </div>
                </body>
            </html>
            """

@auth_bp.route("/reset_password/<token>", methods=["POST"])
def reset_password(token):
    data = request.get_json()
    new_password = data.get("new_password")

    user = User.verify_reset_token(token)
    if not user:
        return jsonify({"success": False, "message": "Invalid or expired token"}), 400

    user.set_password(new_password)
    db.session.commit()
    return jsonify({"success": True, "message": "Password reset successful"}), 200