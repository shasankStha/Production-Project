import React from "react";
import { logout } from "../utils/Auth";

const UserDashboard = () => {
  return (
    <div>
      <h2>User Dashboard</h2>
      <p>Welcome, User!</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
};

export default UserDashboard;
