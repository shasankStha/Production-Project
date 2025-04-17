import React, { useState } from "react";
import Sidebar from "./Sidebar";
import "../styles/Header.css";
import UserChangePassword from "./UserChangePassword";
import { FaKey, FaSignOutAlt } from "react-icons/fa";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { isAdmin } from "../utils/Auth";

const Header = ({ title }) => {
  const { logout } = useAuth();
  const [showSidebar, setShowSidebar] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();

  const toggleSidebar = () => setShowSidebar((prev) => !prev);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header className="header-container">
      {isAdmin() && (
        <div className="header-left">
          <button className="sidebar-toggle" onClick={toggleSidebar}>
            &#9776;
          </button>
          <Sidebar isOpen={showSidebar} onClose={() => setShowSidebar(false)} />
        </div>
      )}

      <div className="header-center">
        <h2 className="page-title">{title}</h2>
      </div>

      <div className="header-right">
        <button className="header-action-btn" onClick={() => setIsModalOpen(true)}>
          <FaKey className="action-icon" />
          <span>Password</span>
        </button>

        <UserChangePassword
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
        />

        <button className="header-action-btn" onClick={handleLogout}>
          <FaSignOutAlt className="action-icon" />
          <span>Logout</span>
        </button>
      </div>
    </header>
  );
};

export default Header;
