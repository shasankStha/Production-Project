import React, { useState, useEffect } from "react";
import io from "socket.io-client";
import VideoFeed from "../components/VideoFeed";
import Header from "../components/Header";
import "../styles/Register.css";

const socket = io("http://127.0.0.1:5000");

const Register = () => {
  const [username, setUsername] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
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
    if (!username || !firstName || !lastName || !email) {
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
          email
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
    <div className="register-page">
      <div className="register-content">
      <Header title="Register" />

        <div className="register-main">
          <div className="register-video">
            <VideoFeed attendance={false} />
          </div>

          <div className="register-form">
            <h2>Fill this form</h2>
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter username"
              />
            </div>
            <div className="form-group">
              <label>First Name</label>
              <input
                type="text"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                placeholder="Enter first name"
              />
            </div>
            <div className="form-group">
              <label>Last Name</label>
              <input
                type="text"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                placeholder="Enter last name"
              />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter email"
              />
            </div>
            <button
              className="register-button"
              onClick={registerUser}
              disabled={loading}
            >
              {loading ? "Registering..." : "Register"}
            </button>

            {message && (
              <div
                className={`status-message ${
                  message.includes("successfully") ? "success" : "error"
                }`}
              >
                {message}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
