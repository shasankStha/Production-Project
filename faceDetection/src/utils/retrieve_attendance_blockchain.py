import json
from dotenv import load_dotenv
from datetime import datetime
from src.services.ipfs_store import ipfs_get_data 
from src.blockchain.get_cid_from_blockchain import get_attendance
from src.utils.extensions import db
from src.models.attendance_summary import AttendanceSummary
from src.models.blockchain_record import BlockchainRecord

load_dotenv()

def retrieve_attendance_summary_and_data(attendance_summary_date):
    """Retrieves the attendance record from blockchain and validates the date."""
    attendance_summary = db.session.query(AttendanceSummary).filter_by(attendance_date=attendance_summary_date).first()

    if not attendance_summary:
        return {"error": "Attendance summary for the given date not found."}
    
    blockchain_record = db.session.query(BlockchainRecord).filter_by(summary_id=attendance_summary.summary_id).first()

    if not blockchain_record:
        return {"error": "Blockchain record for the given attendance summary not found."}

    record_id = blockchain_record.blockchain_record_id

    if not record_id:
        return {"error": "Record is not yet been written in blockchain."}
    
    blockchain_data = get_attendance(record_id)

    if blockchain_record is None:
        return {"error": "Blockchain record not found."}

    blockchain_date = blockchain_data["date"]
    if blockchain_date != str(attendance_summary_date):
        print(f"[ERROR] Date mismatch: Blockchain date ({blockchain_date}) does not match the attendance summary date ({attendance_summary_date}).")
        return {"error": "Date mismatch between blockchain and attendance summary."}

    cid = blockchain_data["cid"]
    ipfs_data = ipfs_get_data(cid)

    if ipfs_data is None:
        return {"error": "Failed to retrieve data from IPFS."}

    return {"ipfs_data": ipfs_data, "cid": cid, "date": blockchain_date}

