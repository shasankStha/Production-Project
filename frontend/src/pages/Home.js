import React from "react";
import { useNavigate } from "react-router-dom";
import VideoFeed from "../components/VideoFeed";
import "../styles/Home.css";

const Home = () => {
    const navigate = useNavigate();

    return (
        <div className="home-container">
            <h1>Facial Recognition Attendance System</h1>
            <VideoFeed />
            <button onClick={() => navigate("/register")} className="register-btn">
                Register
            </button>
        </div>
    );
};

export default Home;
