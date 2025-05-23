from flask_socketio import SocketIO
from concurrent.futures import ThreadPoolExecutor
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
import os
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler

# Initialize SocketIO
socketio = SocketIO()

# Initialize ThreadPool
max_workers = max(2, os.cpu_count() // 2)
thread_pool = ThreadPoolExecutor(max_workers=max_workers)

# Create the SQLAlchemy object
db = SQLAlchemy()

bcrypt = Bcrypt()
jwt = JWTManager()

mail = Mail()

scheduler = BackgroundScheduler()