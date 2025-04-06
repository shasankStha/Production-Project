import React from "react";
import "../styles/VideoFeed.css";

const VideoFeed = ({ attendance }) => {
  return (
    <div className="video-container">
      <img src={`http://127.0.0.1:5000/video_feed?attendance=false`} alt="Live Video Feed" />
    </div>
  );
}

export default VideoFeed;
