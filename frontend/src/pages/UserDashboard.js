import React from "react";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import Footer from "../components/Footer";
import "../styles/UserDashboard.css";

const UserDashboard = () => {
  return (
    <div className="dashboard-container">
      <Sidebar />
      <div className="main-content">
        <Header />
        <div className="content">
          <h2>User Dashboard</h2>
          <p>Welcome to your dashboard.</p>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default UserDashboard;
