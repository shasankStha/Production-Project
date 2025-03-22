import React from "react";
import "../styles/Attendance.css";
import "../components/VideoFeed";
import VideoFeed from "../components/VideoFeed";

const Attendance=()=>{
    return (
        <div className="home-container">
            <h1>Facial Recognition Attendance System</h1>
            <VideoFeed attendance={true}/>
        </div>
    );
}

export default Attendance;
