import React from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const UserDashboard = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div>
      <h2>User Dashboard</h2>
      <p>Welcome, User!</p>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default UserDashboard;
