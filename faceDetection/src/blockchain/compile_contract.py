import json
from solcx import compile_standard, install_solc

# Install a specific Solidity compiler version if needed
install_solc('0.8.0')

with open("/Users/shashrestha/Documents/Shasank/Production Project/Production-Project/faceDetection/src/blockchain/contracts/AttendanceRecord.sol", "r") as file:
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

# Save the compiled contract to a JSON file
with open("/Users/shashrestha/Documents/Shasank/Production Project/Production-Project/faceDetection/src/blockchain/compiled/AttendanceRecord.json", "w") as f:
    json.dump(compiled_sol, f, indent=2)

print("Contract compiled successfully!")
