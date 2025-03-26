import React from "react";
import { useNavigate } from "react-router-dom";
import VideoFeed from "../components/VideoFeed";
import "../styles/AdminDashboard.css"
import Sidebar from "../components/Sidebar";

const AdminDashboard = () => {
  const navigate = useNavigate();

  return (
    <div>
      <Sidebar/>
      <h2>Admin Dashboard</h2>
      <p>Welcome, Admin!</p>
      <div className="home-container">
        <h1>Facial Recognition Attendance System</h1>
        <VideoFeed attendance={true} />
        <button onClick={() => navigate("/register")} className="register-btn">
          Register
        </button>
        <button
          onClick={() => navigate("/attendance")}
          className="attendance-btn"
        >
          Attendance
        </button>
      </div>
    </div>
  );
};

export default AdminDashboard;
