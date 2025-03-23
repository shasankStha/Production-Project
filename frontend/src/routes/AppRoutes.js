import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Register from "../pages/Register";
import Attendance from "../pages/Attendance";
import Login from "../components/Login";
import AdminDashboard from "../pages/AdminDashboard";
import UserDashboard from "../pages/UserDashboard";
import { useAuth } from "../context/AuthContext";

function AppRoutes() {
  const { user } = useAuth();

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />

        <Route
          path="/register"
          element={
            user?.role === "admin" ? (
              <Register />
            ) : (
              <Navigate to="/login"></Navigate>
            )
          }
        />
        <Route
          path="/attendance"
          element={
            user?.role === "admin" ? (
              <Attendance />
            ) : (
              <Navigate to="/login"></Navigate>
            )
          }
        />

        <Route
          path="/admin-dashboard"
          element={
            user?.role === "admin" ? (
              <AdminDashboard />
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/user-dashboard"
          element={
            user && user.role !== "admin" ? (
              <UserDashboard />
            ) : (
              <Navigate to="/login" />
            )
          }
        />
      </Routes>
    </Router>
  );
}

export default AppRoutes;
