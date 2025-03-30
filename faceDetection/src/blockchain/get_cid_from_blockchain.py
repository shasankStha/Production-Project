import json
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

def get_attendance(record_id):
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
    assert w3.is_connected(), "Failed to connect to Ganache!"

    with open("/Users/shashrestha/Documents/Shasank/Production Project/Production-Project/faceDetection/src/blockchain/compiled/deployed_AttendanceRecord.json", "r") as f:
        deployed_data = json.load(f)

    contract_address = deployed_data["address"]
    abi = deployed_data["abi"]
    attendance_contract = w3.eth.contract(address=contract_address, abi=abi)

    try:
        record = attendance_contract.functions.records(record_id).call()
        cid, date_str = record
        print(f"[INFO] CID: {cid}, Date: {date_str}")
        return {"cid": cid, "date": date_str}
    except Exception as e:
        print(f"[ERROR] Failed to retrieve record: {e}")
        return None
    
if __name__ == "__main__":
    get_attendance(1)