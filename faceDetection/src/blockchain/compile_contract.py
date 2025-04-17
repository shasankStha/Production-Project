import json
from solcx import compile_standard, install_solc
import os

# Install a specific Solidity compiler version if needed
install_solc('0.8.0')

base_dir = os.path.dirname(os.path.abspath(__file__))
contract_dir = os.path.join(base_dir, 'contracts')
contract_file_path = os.path.join(contract_dir, 'AttendanceRecord.sol')

with open(contract_file_path, "r") as file:
    attendance_record_source = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"AttendanceRecord.sol": {"content": attendance_record_source}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

compiled_dir = os.path.join(base_dir, 'compiled')
compiled_file_path = os.path.join(compiled_dir, 'AttendanceRecord.json')

# Save the compiled contract to a JSON file
with open(compiled_file_path, "w") as f:
    json.dump(compiled_sol, f, indent=2)

print("Contract compiled successfully!")
