import React from "react";
import "../styles/AdminDashboard.css"
import Sidebar from "../components/Sidebar";
import AdminAttendanceTable from "../components/AdminAttendanceTable";
import "../styles/AdminAttendanceTable.css"

const AdminDashboard = () => {

  return (
    <div>
      <Sidebar/>
      <h2>Admin Dashboard</h2>
      <p>Welcome, Admin!</p>
      <div className="home-container">
        <h1>Facial Recognition Attendance System</h1>
        <AdminAttendanceTable />
      </div>
    </div>
  );
};

export default AdminDashboard;
