import React from "react";
import "../styles/VideoFeed.css"; // Add styles if needed

const VideoFeed = () => {
    return (
        <div className="video-container">
            <h2>Live Video Feed</h2>
            <img src="http://127.0.0.1:5000/video_feed" alt="Live Video Feed" />
        </div>
    );
};

export default VideoFeed;
