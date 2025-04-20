import { React, useState } from "react";
import "../styles/Attendance.css";
import Header from "../components/Header";
import VideoFeed from "../components/VideoFeed";

const Attendance = () => {
  const [attendanceActive, setAttendanceActive] = useState(false);

  const toggleAttendance = async () => {
    const newStatus = !attendanceActive;
    setAttendanceActive(newStatus);

    try {
      // Ping the video_feed endpoint to trigger backend attendance mode switch
      await fetch(`http://127.0.0.1:5000/video_feed?attendance=${newStatus}`, {
        method: "GET",
      });
    } catch (error) {
      console.error("Error toggling attendance:", error);
    }
  };

  return (
    <div className="home-container">
      <Header title="Take Attendance" />
      <div className="video-wrapper">
        <VideoFeed attendance={attendanceActive} />
      </div>

      <div className="attendance-controls">
        <button
          className={`start-stop-btn ${attendanceActive ? "stop" : "start"}`}
          onClick={toggleAttendance}
        >
          {attendanceActive ? "Stop Attendance" : "Start Attendance"}
        </button>
      </div>
    </div>
  );
};

export default Attendance;
