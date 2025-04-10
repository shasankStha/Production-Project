import json
from datetime import datetime
from src.models.attendance import Attendance
from src.models.attendance_summary import AttendanceSummary
from src.models.blockchain_record import BlockchainRecord
from src.utils.extensions import db
import os
import subprocess
import tempfile
import time
import platform
from src.blockchain.record_on_chain import record_attendance

def store_attendance_ipfs(date_str):
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as e:
        print(f"Invalid date format: {e}")
        return None

    try:
        attendance_records = (
            db.session.query(Attendance)
            .filter(db.func.date(Attendance.timestamp) == target_date)
            .all()
        )
        if not attendance_records:
            return
        
        attendance_summary = (
            db.session.query(AttendanceSummary)
            .filter_by(attendance_date=target_date)
            .first()
        )
        
        attendance_data = []
        for record in attendance_records:
            attendance_data.append({
                "attendance_id": record.attendance_id,
                "user_id": record.user_id,
                "summary_id": record.summary_id,
                "timestamp": record.timestamp.isoformat()
            })

        blockchain_date_str = str(attendance_summary.attendance_date)

        
        # Prepare the data to store
        data_to_store = {
            "summary_id": attendance_summary.summary_id,
            "date": date_str,
            "attendance_records": attendance_data
        }
        
        # Storing data in ipfs
        json_data = json.dumps(data_to_store)
        cid = ipfs_add_json(json_data)
        if cid is None:
            print("[ERROR] Failed to pin JSON to IPFS.")
            return None

        print(f"[INFO] Data pinned to IPFS with CID: {cid}")
        
        if attendance_summary:
            attendance_summary.ipfs_cid = cid
            db.session.commit()
            print("[INFO] Attendance summary updated with IPFS CID.")
        
        # Save the IPFS CID and date to the blockchain
        tx_receipt, tx_hash, blockchain_record_id = record_attendance(cid, blockchain_date_str)
        if tx_receipt:
            print("[INFO] Blockchain record created successfully.")

        blockchain_record = BlockchainRecord(
            summary_id=attendance_summary.summary_id,
            transaction_hash=tx_hash,
            blockchain_record_id=blockchain_record_id
        )

        db.session.add(blockchain_record)
        db.session.commit()

        if attendance_summary and blockchain_record:
            attendance_summary.blockchain_records.append(blockchain_record)
            db.session.commit()
            print("[INFO] Attendance summary updated with Blockchain Record ID.")

        return tx_receipt
    except Exception as e:
        print(f"[ERROR] An error occurred while storing attendance for {date_str}: {str(e)}")
        return None

def is_ipfs_daemon_running():
    """Check if the IPFS daemon is running."""
    try:
        subprocess.run(["ipfs", "swarm", "peers"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True
    except subprocess.CalledProcessError:
        return False

def start_ipfs_daemon():
    """Start the IPFS daemon."""
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["ipfs", "daemon"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(["ipfs", "daemon"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Wait briefly to allow the daemon to start
        time.sleep(5)
        return is_ipfs_daemon_running()
    except Exception as e:
        print(f"[ERROR] Failed to start IPFS daemon: {e}")
        return False

def ipfs_add_json(json_data):

    if not is_ipfs_daemon_running():
        print("[INFO] IPFS daemon is not running. Attempting to start it...")
        if not start_ipfs_daemon():
            print("[ERROR] Unable to start IPFS daemon.")
            return None
        
    try:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as tmp_file:
            tmp_file.write(json_data)
            tmp_file_path = tmp_file.name

        cid = subprocess.check_output(
            ["ipfs", "add", "-q", tmp_file_path],
            stderr=subprocess.STDOUT,
            text=True
        ).strip()

        os.remove(tmp_file_path)
        return cid
    
    except subprocess.CalledProcessError as e:
        print("[ERROR] Failed to add JSON data to IPFS via CLI:")
        print(e.output)
        return None
    

def ipfs_get_data(cid):
    if not is_ipfs_daemon_running():
        print("[INFO] IPFS daemon is not running. Attempting to start it...")
        if not start_ipfs_daemon():
            print("[ERROR] Unable to start IPFS daemon.")
            return None
    try:
        data = subprocess.check_output(
            ["ipfs", "cat", cid],
            stderr=subprocess.STDOUT,
            text=True
        )
        return data
    except subprocess.CalledProcessError as e:
        print("[ERROR] Failed to retrieve data from IPFS via CLI:")
        print(e.output)
        return None
    

