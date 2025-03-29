import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import AdminAttendanceTable from "../components/AdminAttendanceTable";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "../styles/AdminDashboard.css";

const AdminDashboard = () => {
  const [attendanceData, setAttendanceData] = useState({});
  const [selectedDate, setSelectedDate] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    fetchAttendanceRecords();
  }, []);

  const fetchAttendanceRecords = async () => {
    try {
      const response = await fetch("http://localhost:5000/admin/attendance_records");
      const data = await response.json();

      if (data.success) {
        setAttendanceData(data.attendance_records);
      }
    } catch (err) {
      console.error("Error fetching data:", err);
    }
  };

  const highlightDates = ({ date }) => {
    const dateString = date.toISOString().split("T")[0];
    return attendanceData[dateString] ? "highlight" : null;
  };

  const handleDateClick = (date) => {
    const dateString = date.toISOString().split("T")[0];
    if (attendanceData[dateString]) {
      setSelectedDate(dateString);
      setModalOpen(true);
    }
  };

  return (
    <div className="admin-container">
      <Sidebar />
      <h2 className="dashboard-title">Admin Dashboard</h2>

      <div className="calendar-container">
        <h3>Select a Date</h3>
        <Calendar tileClassName={highlightDates} onClickDay={handleDateClick} />
      </div>

      {modalOpen && selectedDate && (
        <div className="modal">
          <div className="modal-content">
            <span className="close" onClick={() => setModalOpen(false)}>&times;</span>
            <h3>Attendance for {selectedDate}</h3>
            <AdminAttendanceTable records={attendanceData[selectedDate]} />
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
