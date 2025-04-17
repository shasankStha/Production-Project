import React, { useState,useRef,useEffect, useCallback } from "react";
import axios from "axios";
import { getToken } from "../utils/Auth";
import "../styles/UserChangePassword.css";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { removeToken } from "../utils/Auth";


const UserChangePassword = ({ isOpen, onClose }) => {
  const navigate = useNavigate();
  const modalRef = useRef();

  const [form, setForm] = useState({
    current_password: "",
    new_password: "",
    confirm_password: "",
  });

  const [showPassword, setShowPassword] = useState({
    current: false,
    new: false,
    confirm: false,
  });

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const togglePasswordVisibility = (field) => {
    setShowPassword({ ...showPassword, [field]: !showPassword[field] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    if (form.new_password !== form.confirm_password) {
      setError("New password and confirm password do not match");
      return;
    }

    try {
      const token = getToken();
      const res = await axios.put(
        "http://localhost:5000/auth/change_password",
        {
          current_password: form.current_password,
          new_password: form.new_password,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      
      setMessage(res.data.message);
      if (res.data.success) {
        removeToken();
        navigate("/login");
      } else {
        setMessage(res.data.message || "Password changed failed");
        setForm({ current_password: "", new_password: "", confirm_password: "" });
      }
    } catch (err) {
      setError(err.response?.data?.message || "Failed to change password");
    }
  };

  const handleOutsideClick = useCallback(
    (e) => {
      if (modalRef.current && !modalRef.current.contains(e.target)) {
        onClose();
      }
    },
    [onClose]
  );
  useEffect(() => {
    if (isOpen) {
      document.addEventListener("mousedown", handleOutsideClick);
    } else {
      document.removeEventListener("mousedown", handleOutsideClick);
    }
    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
    };
  }, [isOpen, handleOutsideClick]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content scrollable" ref={modalRef}>
        <div className="modal-header">
          <h3>Change Password</h3>
          <span className="close-btn" onClick={onClose}>&times;</span>
        </div>

        <form onSubmit={handleSubmit} className="change-password-form">
          <label htmlFor="current_password">Current Password</label>
          <div className="password-input-wrapper">
            <input
              type={showPassword.current ? "text" : "password"}
              id="current_password"
              name="current_password"
              value={form.current_password}
              onChange={handleChange}
              required
            />
            <span onClick={() => togglePasswordVisibility("current")}>
              {showPassword.current ? <FaEyeSlash /> : <FaEye />}
            </span>
          </div>

          <label htmlFor="new_password">New Password</label>
          <div className="password-input-wrapper">
            <input
              type={showPassword.new ? "text" : "password"}
              id="new_password"
              name="new_password"
              value={form.new_password}
              onChange={handleChange}
              required
            />
            <span onClick={() => togglePasswordVisibility("new")}>
              {showPassword.new ? <FaEyeSlash /> : <FaEye />}
            </span>
          </div>

          <label htmlFor="confirm_password">Confirm New Password</label>
          <div className="password-input-wrapper">
            <input
              type={showPassword.confirm ? "text" : "password"}
              id="confirm_password"
              name="confirm_password"
              value={form.confirm_password}
              onChange={handleChange}
              required
            />
            <span onClick={() => togglePasswordVisibility("confirm")}>
              {showPassword.confirm ? <FaEyeSlash /> : <FaEye />}
            </span>
          </div>

          <button type="submit">Update Password</button>
          {message && <p className="success-message">{message}</p>}
          {error && <p className="error-message">{error}</p>}
        </form>
      </div>
    </div>
  );
};
export default UserChangePassword;