import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import Register from "../pages/Register";
import Attendance from "../pages/Attendance";
import Login from "../components/Login";
import AdminDashboard from "../pages/AdminDashboard";
import UserDashboard from "../pages/UserDashboard";
import { isAdmin } from "../utils/Auth";

function AppRoutes() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/attendance" element={<Attendance />} />
        <Route path="/login" element={<Login />} />

        <Route
          path="/admin-dashboard"
          element={isAdmin() ? <AdminDashboard /> : <Login />}
        />
        <Route
          path="/user-dashboard"
          element={!isAdmin() ? <UserDashboard /> : <Login />}
        />
      </Routes>
    </Router>
  );
}

export default AppRoutes;
