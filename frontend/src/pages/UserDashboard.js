import React, { useState, useEffect } from "react";
import Calendar from "react-calendar";
import 'react-calendar/dist/Calendar.css';
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import Footer from "../components/Footer";
import "../styles/UserDashboard.css";
import { getToken } from "../utils/Auth";

const UserDashboard = () => {
  const [attendanceDates, setAttendanceDates] = useState([]);

  useEffect(() => {
    fetchAttendanceDates();
  }, []);

  const fetchAttendanceDates = async () => {
    try {
      const token = getToken();
      const response = await fetch("http://localhost:5000/user/attendance_dates", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const data = await response.json();

      if (data.success) {
        setAttendanceDates(data.attendance_dates.map(date => new Date(date)));
      }
    } catch (err) {
      console.error("Error fetching attendance dates:", err);
    }
  };

  const tileClassName = ({ date, view }) => {
    if (view === 'month') {
      const isMarked = attendanceDates.some(attDate =>
        attDate.toDateString() === date.toDateString()
      );
      return isMarked ? 'highlight' : null;
    }
  };

  return (
    <div className="dashboard-container">
      <Sidebar />
      <div className="main-content">
        <div className="attendance-container">
          <h2 className="dashboard-title">User Dashboard</h2>
          <div className="calendar-container">
            <Calendar tileClassName={tileClassName} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;
