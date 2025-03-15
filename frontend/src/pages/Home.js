import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Home.css";
import "../components/VideoFeed";
// import VideoFeed from "../components/VideoFeed";

const Home=()=>{
    const navigate = useNavigate();

    return (
        <div className="home-container">
            <h1>Facial Recognition Attendance System</h1>
            {/* <VideoFeed attendance={true}/> */}
            <button onClick={() => navigate("/register")} className="register-btn">
                Register
            </button>
            <button onClick={() => navigate("/attendance")} className="attendance-btn">
                Attendance
            </button>
        </div>
    );
}

export default Home;
