import React, { useState, useEffect, useCallback } from "react";
import { useLocation } from "react-router-dom";
import AdminAttendanceTable from "../components/AdminAttendanceTable";
import Header from "../components/Header";
import "../styles/AttendanceRecords.css";

const AttendanceRecords = () => {
  const location = useLocation();
  const [searchQuery, setSearchQuery] = useState("");
  const [searchStartDate, setSearchStartDate] = useState("");
  const [searchEndDate, setSearchEndDate] = useState("");
  const [attendanceSummary, setAttendanceSummary] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);

  useEffect(() => {
    if (!searchStartDate && !searchEndDate) {
      (async () => {
        try {
          const res = await fetch(
            "http://localhost:5000/admin/attendance_summary"
          );
          const data = await res.json();
          if (data.success) {
            const sorted = data.attendance_summary.sort(
              (a, b) => new Date(a) - new Date(b)
            );
            setAttendanceSummary(sorted);
            setSearchStartDate(sorted[0]);
            setSearchEndDate(sorted[sorted.length - 1]);
          }
        } catch (err) {
          console.error("Error fetching attendance summary:", err);
        }
      })();
    }
  }, [searchStartDate, searchEndDate]);
  const performSearch = useCallback(
    async (query) => {
      setSearchLoading(true);
      try {
        const url = `http://localhost:5000/admin/search_attendance?query=${encodeURIComponent(
          query
        )}&start_date=${searchStartDate}&end_date=${searchEndDate}`;
        const res = await fetch(url);
        const data = await res.json();
        setSearchResults(data.success ? data.attendance_records : []);
      } catch (err) {
        console.error("Error during search:", err);
        setSearchResults([]);
      } finally {
        setSearchLoading(false);
      }
    },
    [searchStartDate, searchEndDate]
  );

  useEffect(() => {
    const nameParam = new URLSearchParams(location.search).get("name");
    if (nameParam && searchStartDate && searchEndDate) {
      setSearchQuery(nameParam); 
      performSearch(nameParam);
    }
  }, [location.search, searchStartDate, searchEndDate, performSearch]);

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
        
        <label htmlFor="startDate">Start Date:</label>
        <input
          type="date"
          value={searchStartDate}
          onChange={(e) => setSearchStartDate(e.target.value)}
          min={attendanceSummary[0]}
          max={attendanceSummary[attendanceSummary.length - 1]}
        />

        <label htmlFor="endDate">End Date:</label>
        <input
          type="date"
          value={searchEndDate}
          onChange={(e) => setSearchEndDate(e.target.value)}
          min={attendanceSummary[0]}
          max={attendanceSummary[attendanceSummary.length - 1]}
        />
        <button onClick={() => performSearch(searchQuery)}>Search</button>
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
