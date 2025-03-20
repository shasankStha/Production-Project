from flask import Flask
from flask_cors import CORS
from src.utils.extensions import socketio
from src.routes.register import register_bp
from src.routes.video import video_bp

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(register_bp)
app.register_blueprint(video_bp)

# Initialize SocketIO with the app
socketio.init_app(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return "WebSocket Server Running"

@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

if __name__ == "__main__":
    socketio.run(app)