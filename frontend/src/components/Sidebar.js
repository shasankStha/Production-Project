import {React, useEffect} from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  FaTimes,
  FaHome,
  FaUser,
  FaClipboardList,
  FaSignOutAlt,
  FaList,
  FaUserCog
} from "react-icons/fa";
import { useAuth } from "../context/AuthContext";
import "../styles/Sidebar.css";
const Sidebar = ({ isOpen, onClose }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  // const [isOpen, setIsOpen] = useState(false);

  const handleLogout = () => {
    logout();
    onClose();  
    navigate("/login");
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        isOpen &&
        !event.target.closest(".sidebar") &&
        !event.target.closest(".hamburger-menu")
      ) {
        onClose();
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen, onClose]);

  return (
    <div className={`sidebar ${isOpen ? "open" : ""}`}>
      <div className="close-btn" onClick={onClose}>
        <FaTimes />
      </div>
      <ul>
        <li>
          <Link
            to={user?.role === "admin" ? "/admin-dashboard" : "/user-dashboard"}
            onClick={onClose}
          >
            <FaHome className="icon" />
            <span>Dashboard</span>
          </Link>
        </li>

        {user?.role === "admin" && (
          <>
            <li><a href="/attendance-records" onClick={onClose}><FaClipboardList className="icon" /><span>Attendance Records</span></a></li>
            <li><a href="/admin/users" onClick={onClose}><FaUserCog className="icon" /><span>User Management</span></a></li>
            <li><a href="/register" onClick={onClose}><FaUser className="icon" /><span>Register</span></a></li>
            <li><a href="/attendance" onClick={onClose}><FaList className="icon" /><span>Attendance</span></a></li>
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
  );
};

export default Sidebar;
