import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  FaBars,
  FaTimes,
  FaHome,
  FaUser,
  FaClipboardList,
  FaSignOutAlt,
} from "react-icons/fa";
import { useAuth } from "../context/AuthContext";
import "../styles/Sidebar.css";

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const toggleSidebar = () => {
    setIsOpen((prev) => !prev);
  };

  const handleLogout = () => {
    logout();
    setIsOpen(false);
    navigate("/login");
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        isOpen &&
        !event.target.closest(".sidebar") &&
        !event.target.closest(".hamburger-menu")
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  return (
    <>
      <div
        className={`hamburger-menu ${isOpen ? "hidden" : ""}`}
        onClick={toggleSidebar}
      >
        <FaBars />
      </div>

      <div className={`sidebar ${isOpen ? "open" : ""}`}>
        <div className="close-btn" onClick={toggleSidebar}>
          <FaTimes />
        </div>

        <ul>
          <li>
            <Link
              to={
                user?.role === "admin" ? "/admin-dashboard" : "/user-dashboard"
              }
            >
              <FaHome className="icon" />
              <span>Dashboard</span>
            </Link>
          </li>

          {user?.role === "admin" && (
            <>
              <li>
                <a href="/register">
                  <FaUser className="icon" />
                  <span>Register</span>
                </a>
              </li>
              <li>
                <a href="/attendance">
                  <FaClipboardList className="icon" />
                  <span>Attendance</span>
                </a>
              </li>
            </>
          )}

          <li>
            <div className="logout-btn" onClick={handleLogout}>
              <FaSignOutAlt className="icon" />
              <span>Logout</span>
            </div>
          </li>
        </ul>
      </div>
    </>
  );
};

export default Sidebar;
