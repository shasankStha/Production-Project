from datetime import datetime
from src.services.ipfs_store import store_attendance_ipfs
from config.config import SCHEDULE_HOUR, SCHEDULE_MINUTE
from src.utils.extensions import scheduler


def schedule_ipfs_store(app):
    """Triggers storing attendance data in IPFS and blockchain at a specific time."""
    with app.app_context():  # Ensure Flask context is available
        today_str = datetime.today().strftime('%Y-%m-%d')
        store_attendance_ipfs(today_str)

def start_scheduler(app):
    """Start the scheduler and pass Flask app."""
    scheduler.add_job(schedule_ipfs_store, 'cron', hour=SCHEDULE_HOUR, minute=SCHEDULE_MINUTE, args=[app])
    scheduler.start()
