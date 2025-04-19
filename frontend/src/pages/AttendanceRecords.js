import React, { useState, useEffect } from "react";
import AdminAttendanceTable from "../components/AdminAttendanceTable";
import "../styles/AttendanceRecords.css";
import Header from "../components/Header";
import { useLocation } from "react-router-dom";           

const AttendanceRecords = () => {
  const location = useLocation(); 
  const [searchQuery, setSearchQuery] = useState("");
  const [searchStartDate, setSearchStartDate] = useState("");
  const [searchEndDate, setSearchEndDate] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [attendanceSummary, setAttendanceSummary] = useState([]);

  const [urlName, setUrlName] = useState("");


  useEffect(() => {
    if (!searchStartDate && !searchEndDate) {
      const fetchAttendanceSummary = async () => {
        try {
          const res = await fetch("http://localhost:5000/admin/attendance_summary");
          const data = await res.json();
          if (data.success) {
            const sortedDates = data.attendance_summary.sort(
              (a, b) => new Date(a) - new Date(b)
            );
            setAttendanceSummary(sortedDates);
            if (data.attendance_summary.length > 0) {
              const startDate = data.attendance_summary[0];
              const endDate = data.attendance_summary[data.attendance_summary.length - 1];
              setSearchStartDate(startDate);
              setSearchEndDate(endDate);
            }
          }
        } catch (err) {
          console.error("Error fetching attendance summary:", err);
        }
      };
      fetchAttendanceSummary();
    }
  }, [searchStartDate, searchEndDate]);

  useEffect(() => {
    const nameParam = new URLSearchParams(location.search).get("name");
    if (nameParam && searchStartDate && searchEndDate) {
      setSearchQuery(nameParam);
      performSearch(nameParam);
    }
  }, [location.search, searchStartDate, searchEndDate]);

  useEffect(() => {
    const nameParam = new URLSearchParams(location.search).get("name");
    if (nameParam) {
      setUrlName(nameParam);
      setSearchQuery(nameParam);
    }
  }, [location.search]);

  const performSearch = async () => {
    setSearchLoading(true);
    try {
      const url = `http://localhost:5000/admin/search_attendance?query=${encodeURIComponent(
        searchQuery
      )}&start_date=${searchStartDate}&end_date=${searchEndDate}`;
      const res = await fetch(url);
      const data = await res.json();
      if (data.success) {
        setSearchResults(data.attendance_records);
      } else {
        setSearchResults([]);
      }
    } catch (err) {
      console.error("Error during search:", err);
    } finally {
      setSearchLoading(false);
    }
  };

  return (
    <div className="attendance-records-container">
      <Header title="Attendance Records" />
      <div className="search-box">
        <input
          type="text"
          placeholder="Search by username or name"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <input
          type="date"
          value={searchStartDate}
          onChange={(e) => setSearchStartDate(e.target.value)}
          min={attendanceSummary[0]}
          max={attendanceSummary[attendanceSummary.length - 1]} 
        />
        <input
          type="date"
          value={searchEndDate}
          onChange={(e) => setSearchEndDate(e.target.value)}
          min={attendanceSummary[0]}
          max={attendanceSummary[attendanceSummary.length - 1]} 
        />
        <button onClick={performSearch}>Search</button>
      </div>

      {searchLoading ? (
        <p>Loading...</p>
      ) : (
        <div className="attendance-results">
          <AdminAttendanceTable records={searchResults} />
        </div>
      )}
    </div>
  );
};

export default AttendanceRecords;