import {React, useEffect, useState} from "react";
import "../styles/Attendance.css";
import "../components/VideoFeed";
// import VideoFeed from "../components/VideoFeed";
import Sidebar from "../components/Sidebar";

const Attendance=()=>{
    const [videoSrc, setVideoSrc] = useState("");

    useEffect(() => {
        const timestamp = new Date().getTime();
        setVideoSrc(`http://127.0.0.1:5000/video_feed?attendance=true&_=${timestamp}`);
    }, []);
    return (
        <div className="home-container">
            <Sidebar/>
            <h2>Facial Recognition Attendance System</h2>
            <div className="video-wrapper">
            <div className="video-container">
            {videoSrc && (
                        <img src={videoSrc} alt="Live Video Feed" />
                    )}
            </div>
            </div>
        </div>
    );
}

export default Attendance;
