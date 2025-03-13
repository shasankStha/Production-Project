import React, { useState } from "react";
import VideoFeed from "../components/VideoFeed";
import "../styles/Register.css";

function Register() {
    const [userId, setUserId] = useState("");
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const registerUser = async () => {
        if (!userId || !name || !email) {
            setMessage("All fields are required!");
            return;
        }

        setLoading(true);
        setMessage("");

        try {
            const response = await fetch("http://127.0.0.1:5000/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId, name, email }),
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
            <h1>Register</h1>
            <VideoFeed />
            <input type="text" placeholder="User ID" value={userId} onChange={(e) => setUserId(e.target.value)} />
            <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
            <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <button onClick={registerUser} disabled={loading}>{loading ? "Registering..." : "Register"}</button>
            {message && <h3 className="message">{message}</h3>}
        </div>
    );
}

export default Register;
