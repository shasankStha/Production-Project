// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AttendanceRecord {
    struct Record {
        string cid;
        string date;
    }
    
    Record[] public records;
    
    event RecordAdded(uint indexed recordId, string cid, string date);
    
    /// @notice Adds a new attendance record.
    /// @param _cid The IPFS CID.
    /// @param _date The attendance date as a string.
    function addRecord(string memory _cid, string memory _date) public {
        records.push(Record(_cid, _date));
        emit RecordAdded(records.length - 1, _cid, _date);
    }
}
