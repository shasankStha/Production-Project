import React from "react";
import "../styles/Attendance.css";
import "../components/VideoFeed";
import VideoFeed from "../components/VideoFeed";
import Sidebar from "../components/Sidebar";

const Attendance=()=>{
    return (
        <div className="home-container">
            <Sidebar/>
            <h1>Facial Recognition Attendance System</h1>
            <VideoFeed attendance={true}/>
        </div>
    );
}

export default Attendance;
