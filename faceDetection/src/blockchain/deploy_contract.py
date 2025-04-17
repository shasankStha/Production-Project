import json
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
assert w3.is_connected(), "Failed to connect to Ganache!"
w3.eth.default_account = os.getenv('GANACHE_ADDRESS')

#Managing file paths
base_dir = os.path.dirname(os.path.abspath(__file__))
compiled_dir = os.path.join(base_dir, 'compiled')
compiled_file_path = os.path.join(compiled_dir, 'AttendanceRecord.json')
deployed_file_path = os.path.join(compiled_dir, 'deployed_AttendanceRecord.json')

with open(compiled_file_path, "r") as file:
    compiled_contract = json.load(file)

bytecode = compiled_contract["contracts"]["AttendanceRecord.sol"]["AttendanceRecord"]["evm"]["bytecode"]["object"]
abi = compiled_contract["contracts"]["AttendanceRecord.sol"]["AttendanceRecord"]["abi"]

AttendanceRecord = w3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = AttendanceRecord.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = tx_receipt.contractAddress
print("Contract deployed at address:", contract_address)

deployed_data = {
    "address": contract_address,
    "abi": abi
}
with open(deployed_file_path, "w") as f:
    json.dump(deployed_data, f, indent=2)
