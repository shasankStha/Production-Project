import React from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import VideoFeed from "../components/VideoFeed";

const AdminDashboard = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div>
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
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default AdminDashboard;
