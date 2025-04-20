import React, { useState, useEffect } from "react";
import Header from "../components/Header";
import "../styles/UserDashboard.css";
import "../styles/UserChangePassword.css";
import { getToken } from "../utils/Auth";

const UserDashboard = () => {
  const [attendanceDates, setAttendanceDates] = useState([]);
  const [totalSessions, setTotalSessions] = useState(0);

  useEffect(() => {
    fetchAttendanceDates();
  }, []);

  const fetchAttendanceDates = async () => {
    try {
      const token = getToken();
      const response = await fetch("http://localhost:5000/user/attendance_dates", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      if (data.success) {
        setAttendanceDates(data.attendance_dates);
        setTotalSessions(data.total_attendance_days);
      }
    } catch (err) {
      console.error("Error fetching attendance dates:", err);
    }
  };
  const getMetrics = () => {
    const presentDays = attendanceDates.length;
    const percentage = totalSessions > 0 ? ((presentDays / totalSessions) * 100).toFixed(2) : 0;
    const lastAttended = presentDays > 0 ? attendanceDates.sort().at(-1) : "N/A";
    return { presentDays, percentage, lastAttended };
  };

  const { presentDays, percentage, lastAttended } = getMetrics();

  const generateCalendarGrid = () => {
    const year = 2025;
    const months = Array.from({ length: 12 }, (_, i) =>
      new Date(year, i).toLocaleString("default", { month: "long" })
    );
    const attendanceSet = new Set(attendanceDates);

    return months.map((month, index) => {
      const daysInMonth = new Date(year, index + 1, 0).getDate();
      const dayStatus = [];

      for (let day = 1; day <= daysInMonth; day++) {
        const dateStr = `${year}-${String(index + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
        dayStatus.push(attendanceSet.has(dateStr) ? "P" : "-");
      }

      return (
        <tr key={month}>
          <td>{month}, {year}</td>
          {[...Array(31)].map((_, i) => (
            <td key={i} className={dayStatus[i] === "P" ? "present" : "absent"}>
              {i < daysInMonth ? dayStatus[i] : ""}
            </td>
          ))}
        </tr>
      );
    });
  };

  return (
    <div className="user-dashboard-container">
    <Header title="User Dashboard" />
  <div className="user-main-content">

        <div className="summary-cards">
          <div className="summary-card"><h4>Total Sessions</h4><p>{totalSessions}</p></div>
          <div className="summary-card"><h4>Days Present</h4><p>{presentDays}</p></div>
          <div className="summary-card"><h4>Attendance %</h4><p>{percentage}%</p></div>
          <div className="summary-card"><h4>Last Attended</h4><p>{lastAttended}</p></div>
        </div>

        <div className="user-custom-calendar">
          <table className="custom-calendar-table">
            <thead>
              <tr>
                <th>Month/Year</th>
                {[...Array(31)].map((_, i) => <th key={i}>{i + 1}</th>)}
              </tr>
            </thead>
            <tbody>{generateCalendarGrid()}</tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;
