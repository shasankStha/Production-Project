import json
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()
def record_attendance(cid, date_str):
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
    assert w3.is_connected(), "Failed to connect to Ganache!"

    with open("/Users/shashrestha/Documents/Shasank/Production Project/Production-Project/faceDetection/src/blockchain/compiled/deployed_AttendanceRecord.json", "r") as f:
        deployed_data = json.load(f)
    
    contract_address = deployed_data["address"]
    abi = deployed_data["abi"]

    attendance_contract = w3.eth.contract(address=contract_address, abi=abi)
    
    from_account = os.getenv('GANACHE_ADDRESS')
    
    tx_hash = attendance_contract.functions.addRecord(cid, date_str).transact({
        'from': from_account,
        'gas': 2000000,
        'gasPrice': w3.to_wei('50', 'gwei') 
    })

    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    logs = attendance_contract.events.RecordAdded().process_receipt(tx_receipt)
    if logs and len(logs) > 0:
        record_id = logs[0]['args']['recordId']
    else:
        raise Exception("RecordAdded event not found in transaction receipt")
    
    return tx_receipt, tx_hash.hex(), record_id
