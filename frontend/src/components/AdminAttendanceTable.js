import React, { useEffect, useState } from "react";

const AdminAttendanceTable = () => {
  const [attendanceRecords, setAttendanceRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAttendanceRecords();
  }, []);

  const fetchAttendanceRecords = async () => {
    try {
      const response = await fetch("http://localhost:5000/admin/attendance_records");
      const data = await response.json();

      if (data.success) {
        setAttendanceRecords(data.attendance_records);
      } else {
        setError("Failed to fetch attendance records");
      }
    } catch (err) {
      setError("Error fetching data");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto mt-8 p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-2xl font-bold mb-4">Attendance Records</h2>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full border-collapse border border-gray-300">
            <thead className="bg-gray-100">
              <tr>
                <th className="border p-3">#</th>
                <th className="border p-3">Username</th>
                <th className="border p-3">Full Name</th>
                <th className="border p-3">Date</th>
                <th className="border p-3">Time</th>
              </tr>
            </thead>
            <tbody>
              {attendanceRecords.length > 0 ? (
                attendanceRecords.map((record, index) => (
                  <tr key={record.attendance_id} className="hover:bg-gray-50">
                    <td className="border p-3">{index + 1}</td>
                    <td className="border p-3">{record.username}</td>
                    <td className="border p-3">{record.name}</td>
                    <td className="border p-3">{record.date}</td>
                    <td className="border p-3">{record.time}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="text-center p-4">No attendance records found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default AdminAttendanceTable;
