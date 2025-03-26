from flask_socketio import SocketIO
from concurrent.futures import ThreadPoolExecutor
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
import os

# Initialize SocketIO
socketio = SocketIO()

# Initialize ThreadPool
max_workers = max(2, os.cpu_count() // 2)
thread_pool = ThreadPoolExecutor(max_workers=max_workers)

# Create the SQLAlchemy object
db = SQLAlchemy()

bcrypt = Bcrypt()
jwt = JWTManager()

