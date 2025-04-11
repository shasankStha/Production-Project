import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import AdminAttendanceTable from "../components/AdminAttendanceTable";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "../styles/AdminDashboard.css";

const AdminDashboard = () => {
  const [attendanceSummarySet, setAttendanceSummarySet] = useState(new Set());
  const [selectedDate, setSelectedDate] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [attendanceRecords, setAttendanceRecords] = useState(null);
  const [loading, setLoading] = useState(false);
  const [disclaimer, setDisclaimer] = useState(null);
  const [source, setSource] = useState(null); 


  useEffect(() => {
    fetchAttendanceSummary();
  }, []);

  const fetchAttendanceSummary = async () => {
    try {
      const response = await fetch("http://localhost:5000/admin/attendance_summary");
      const data = await response.json();
  
      if (data.success) {
        setAttendanceSummarySet(new Set(data.attendance_summary));
      }
    } catch (err) {
      console.error("Error fetching attendance summary:", err);
    }
  };

  const fetchAttendanceDetails = async (attendanceDate) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:5000/admin/attendance_records/${attendanceDate}`);
      const data = await response.json();

      if (data.success) {
        setAttendanceRecords(data.attendance_records);
        setSource(data.source);
        setDisclaimer(data.disclaimer);
      }else{
        setAttendanceRecords(null)
        setSource(null);
        setDisclaimer(null);
      }
    } catch (err) {
      console.error("Error fetching detailed attendance records:", err);
    }finally {
      setLoading(false);
    }
  };

  const highlightDates = ({ date }) => {
    const dateString = formatDate(date);
    return attendanceSummarySet.has(dateString) ? "highlight" : null;
  };

  const handleDateClick = (date) => {
    const dateString = formatDate(date);
    if (attendanceSummarySet.has(dateString)) {
      setSelectedDate(dateString);
      fetchAttendanceDetails(dateString);
      setModalOpen(true);
    }
  };

  const formatDate = (date) => {
    const offset = date.getTimezoneOffset();
    const localDate = new Date(date.getTime() - offset * 60 * 1000);
    return localDate.toISOString().split("T")[0];
  };
  

  return (
    <div className="admin-container">
      <Sidebar />
      <h2 className="admin-dashboard-title">Admin Dashboard</h2>

      <div className="admin-calendar-container">
        <h3>Select a Date</h3>
        <Calendar tileClassName={highlightDates} onClickDay={handleDateClick} showNeighboringMonth={false} />
      </div>

      {modalOpen && selectedDate && (
        <div className="modal" onClick={() => setModalOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <span className="close" onClick={() => setModalOpen(false)}>
              &times;
            </span>
            <h3>Attendance for {selectedDate}</h3>
            <div className="modal-body">
            {loading ? (
                <p>Loading records...</p>
              ) : (
                <>
                <AdminAttendanceTable records={attendanceRecords} />
                {source === "postgres" && disclaimer && (
                  <p className="disclaimer">{disclaimer}</p>
                )}
              </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
