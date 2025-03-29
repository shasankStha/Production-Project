import React from "react";
import "../styles/Attendance.css";
import "../components/VideoFeed";
import VideoFeed from "../components/VideoFeed";
import Sidebar from "../components/Sidebar";

const Attendance=()=>{
    return (
        <div className="home-container">
            <Sidebar/>
            <h2>Facial Recognition Attendance System</h2>
            <div className="video-wrapper">
                <VideoFeed attendance={true}/>
            </div>
        </div>
    );
}

export default Attendance;
