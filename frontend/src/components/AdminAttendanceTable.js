import React from "react";
import "../styles/AdminAttendanceTable.css";

const AdminAttendanceTable = ({ records }) => {
  return (
    <div className="table-container">
      <h2 className="table-title">Attendance Records</h2>
      <div className="overflow-x-auto">
        <table className="styled-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Username</th>
              <th>Full Name</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {records.length > 0 ? (
              records.map((record, index) => (
                <tr key={record.attendance_id} className="hover-row">
                  <td>{index + 1}</td>
                  <td>{record.username}</td>
                  <td>{record.name}</td>
                  <td>{record.time}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4" className="text-center">No records found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminAttendanceTable;
