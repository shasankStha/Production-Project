import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "../pages/Login";
import ForgotPassword from "../pages/ForgotPassword";
import ResetPassword from "../pages/ResetPassword";
import AdminDashboard from "../pages/AdminDashboard";
import UserDashboard from "../pages/UserDashboard";
import Register from "../pages/Register";
import Attendance from "../pages/Attendance";
import { useAuth } from "../context/AuthContext";
import AttendanceRecords from "../pages/AttendanceRecords";
import UserManagement from "../pages/UserManagement";
import UserChangePassword from "../components/UserChangePassword";

function AppRoutes() {
  const { user } = useAuth();

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />

        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password/:token" element={<ResetPassword />} />

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
          path="/register"
          element={
            user?.role === "admin" ? <Register /> : <Navigate to="/login" />
          }
        />
        <Route
          path="/attendance-records"
          element={
            user === undefined ? (
              <div>Loading...</div>
            ) : user?.role === "admin" ? (
              <AttendanceRecords />
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/attendance"
          element={
            user?.role === "admin" ? <Attendance /> : <Navigate to="/login" />
          }
        />
        <Route
          path="/admin/users"
          element={
            user?.role === "admin" ? (
              <UserManagement />
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

        <Route path="/change-password" element={<UserChangePassword />} />
      </Routes>
    </Router>
  );
}

export default AppRoutes;
