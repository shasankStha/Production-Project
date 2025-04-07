from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from src.utils.extensions import socketio, db,bcrypt,jwt, mail
from src.routes.register import register_bp
from src.routes.video import video_bp
from src.routes.auth import auth_bp
from src.routes.admin import admin_bp
from src.routes.user import user_bp
from src.models.user import User
from dotenv import load_dotenv
import os
from src.utils.scheduler import start_scheduler
from src.services.ipfs_store import is_ipfs_daemon_running, start_ipfs_daemon

load_dotenv()
migrate = Migrate()
def create_app():
    app = Flask(__name__)
    app.config.from_object("config.config.Config")
    
    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    mail.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(register_bp)
    app.register_blueprint(video_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(user_bp, url_prefix="/user")
    
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
    
    if not is_ipfs_daemon_running():
        print("[INFO] IPFS daemon is not running. Attempting to start it...")
        if not start_ipfs_daemon():
            print("[ERROR] Unable to start IPFS daemon.")
    
    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # db.create_all()
        start_scheduler(app)

    socketio.run(app)