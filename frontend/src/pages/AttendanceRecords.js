import React, { useState, useEffect, useCallback } from "react";
import { useLocation } from "react-router-dom";
import { getToken } from "../utils/Auth";
import AdminAttendanceTable from "../components/AdminAttendanceTable";
import Header from "../components/Header";
import "../styles/AttendanceRecords.css";

const RECORDS_PER_PAGE = 8;

const AttendanceRecords = () => {
  const location = useLocation();
  const [searchQuery, setSearchQuery] = useState("");
  const [searchStartDate, setSearchStartDate] = useState("");
  const [searchEndDate, setSearchEndDate] = useState("");
  const [attendanceSummary, setAttendanceSummary] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);

  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    if (!searchStartDate && !searchEndDate) {
      (async () => {
        try {
          const token = getToken();
          const res = await fetch(
            "http://localhost:5000/admin/attendance_summary",
            {
              headers: { Authorization: `Bearer ${token}` },
            }
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
        if (data.success) {
          setSearchResults(data.attendance_records);
          setCurrentPage(1); // Reset to first page on new search
        } else {
          setSearchResults([]);
        }
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

  const totalPages = Math.ceil(searchResults.length / RECORDS_PER_PAGE);
  const paginatedResults = searchResults.slice(
    (currentPage - 1) * RECORDS_PER_PAGE,
    currentPage * RECORDS_PER_PAGE
  );

  const goToPage = (page) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
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

        <div className="date-picker-row">
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
        </div>

        <button onClick={() => performSearch(searchQuery)}>Search</button>
      </div>

      {searchLoading ? (
        <p>Loading...</p>
      ) : (
        <div className="attendance-results">
          <AdminAttendanceTable records={paginatedResults} />

          {/* Pagination Controls */}
          {searchResults.length > RECORDS_PER_PAGE && (
            <div className="pagination-controls">
              <button
                onClick={() => goToPage(currentPage - 1)}
                disabled={currentPage === 1}
              >
                Prev
              </button>
              {[...Array(totalPages)].map((_, i) => (
                <button
                  key={i}
                  onClick={() => goToPage(i + 1)}
                  className={currentPage === i + 1 ? "active" : ""}
                >
                  {i + 1}
                </button>
              ))}
              <button
                onClick={() => goToPage(currentPage + 1)}
                disabled={currentPage === totalPages}
              >
                Next
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AttendanceRecords;
