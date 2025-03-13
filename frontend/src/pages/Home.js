import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Home.css";

function Home() {
    const navigate = useNavigate();

    return (
        <div className="home-container">
            <h1>Facial Recognition Attendance System</h1>
            <div className="video-container">
                <img src="http://127.0.0.1:5000/video_feed" alt="Live Video Feed" />
            </div>
            <button onClick={() => navigate("/register")} className="register-btn">
                Register
            </button>
        </div>
    );
}

export default Home;
