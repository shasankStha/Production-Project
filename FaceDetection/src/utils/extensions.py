from flask_socketio import SocketIO
from concurrent.futures import ThreadPoolExecutor
import os

# Initialize SocketIO
socketio = SocketIO()

# Initialize ThreadPool
max_workers = max(2, os.cpu_count() // 2)
thread_pool = ThreadPoolExecutor(max_workers=max_workers)

