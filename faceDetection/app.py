from flask import Flask
from flask_cors import CORS
from src.utils.extensions import socketio, db,bcrypt,jwt, mail
from src.routes.register import register_bp
from src.routes.video import video_bp
from src.routes.auth import auth_bp
from src.routes.admin import admin_bp
from src.models.user import User
from dotenv import load_dotenv
import os
# from src.blockchain.get_cid_from_blockchain import get_attendance
# from src.services.ipfs_store import ipfs_get_data

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.config.Config")
    
    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    mail.init_app(app)

    # Register Blueprints
    app.register_blueprint(register_bp)
    app.register_blueprint(video_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    
    @app.route("/")
    def index():
        return "WebSocket Server Running"
    
    @socketio.on("connect")
    def handle_connect():
        print("Client connected")
    
    def handle_disconnect():
        print("Client disconnected")

    with app.app_context():
        db.create_all()
        
        admin_exists = User.query.filter_by(role="admin").first()
        
        if not admin_exists:
            admin_username = os.getenv('ADMIN_USERNAME')
            admin_email = os.getenv('ADMIN_EMAIL')
            admin_password = os.getenv('ADMIN_PASSWORD')
            admin_user = User(
                username=admin_username,
                first_name="Admin",        
                last_name="Admin",
                email=admin_email,         
                role="admin"              
            )
            admin_user.set_password(admin_password)
            db.session.add(admin_user)
            db.session.commit()
            print("Admin created.")
    
    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all() 
        # print(get_attendance(1))    
        # print(ipfs_get_data("QmShjPux1dsKyjJEGKLn1sAJFb4FZqCvj96gcAt9WHyScW"))   
    socketio.run(app)