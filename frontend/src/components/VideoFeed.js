import React from "react";
import "../styles/VideoFeed.css";

const VideoFeed = ({ attendance }) => {
  const url = `http://127.0.0.1:5000/video_feed?attendance=${attendance}`;

  return (
    <div className="video-container">
      <img
        src={url}
        alt="Live Video Feed"
        className="video-feed"
      />
    </div>
  );
};

export default VideoFeed;
