import React from "react";
import { logout } from "../utils/Auth";

const AdminDashboard = () => {
  return (
    <div>
      <h2>Admin Dashboard</h2>
      <p>Welcome, Admin!</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
};

export default AdminDashboard;
