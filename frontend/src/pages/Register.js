import React, { useState, useEffect } from "react";
import io from "socket.io-client";
import VideoFeed from "../components/VideoFeed";
import Sidebar from "../components/Sidebar";
import "../styles/Register.css";

// Connect to the Socket.IO server
const socket = io("http://127.0.0.1:5000");

const Register = () => {
  const [username, setUsername] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    socket.on("registration_status", (data) => {
      setMessage(data.message || data.error);
    });

    return () => {
      socket.off("registration_status");
    };
  }, []);

  const registerUser = async () => {
    if (!username || !firstName || !lastName || !email || !password) {
      setMessage("All fields are required!");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          first_name: firstName,
          last_name: lastName,
          email,
          password,
        }),
      });

      const data = await response.json();
      setMessage(data.message || data.error);
    } catch (error) {
      setMessage("Error connecting to server. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <Sidebar/>
      <div className="video-wrapper">
        <VideoFeed attendance={false} />
      </div>

      <div className="form-scroll-container">
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            placeholder="Enter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>First Name</label>
          <input
            type="text"
            placeholder="Enter first name"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Last Name</label>
          <input
            type="text"
            placeholder="Enter last name"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Email</label>
          <input
            type="email"
            placeholder="Enter email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button className="register-button" onClick={registerUser} disabled={loading}>
          {loading ? "Registering..." : "Register"}
        </button>
        {message && <div className="message">{message}</div>}
      </div>
    </div>
  );
};

export default Register;
