import React, { useState } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import "../styles/Login.css";
import { FaEye, FaEyeSlash } from "react-icons/fa";

const ResetPassword = () => {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [message, setMessage] = useState("");
  const { token } = useParams();
  const navigate = useNavigate();


  const handleReset = async (e) => {
    e.preventDefault();

    if (newPassword !== confirmPassword) {
      setMessage("Password and Confirm Password do not match.");
      return;
    }

    try {
      const response = await axios.post(
        `http://127.0.0.1:5000/auth/reset_password/${token}`,
        { new_password: newPassword }
      );
      if (response.status===200)
        navigate("/login", {
            state: { successMessage: "Password reset successful. Please log in." }
        });      
    } catch (err) {
      setMessage("Invalid or expired token.");
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Set New Password</h2>
        <form onSubmit={handleReset}>
          <div className="input-group password-group">
            <input
              type={showNewPassword ? "text" : "password"}
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="New Password"
              required
            />
            <span
              className="toggle-eye"
              onClick={() => setShowNewPassword((prev) => !prev)}
            >
              {showNewPassword ? <FaEyeSlash /> : <FaEye />}
            </span>
          </div>

          <div className="input-group password-group">
            <input
              type={showConfirmPassword ? "text" : "password"}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm Password"
              required
            />
            <span
              className="toggle-eye"
              onClick={() => setShowConfirmPassword((prev) => !prev)}
            >
              {showConfirmPassword ? <FaEyeSlash /> : <FaEye />}
            </span>
          </div>

          <button type="submit">Reset Password</button>
          {message && <p className="error-message">{message}</p>}
        </form>
      </div>
    </div>
  );
};

export default ResetPassword;
