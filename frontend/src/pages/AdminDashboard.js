import React, { useEffect, useState } from "react";
import Header from "../components/Header";
import AdminAttendanceTable from "../components/AdminAttendanceTable";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "../styles/AdminDashboard.css";
import { Bar, Line, Pie } from "react-chartjs-2";
import ChartDataLabels from "chartjs-plugin-datalabels";
import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  ChartDataLabels
);


const AdminDashboard = () => {
  const [attendanceSummarySet, setAttendanceSummarySet] = useState(new Set());
  const [selectedDate, setSelectedDate] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [attendanceRecords, setAttendanceRecords] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analyticsData, setAnalyticsData] = useState([]);
  const [analyticsLoading, setAnalyticsLoading] = useState(false);
  const [disclaimer, setDisclaimer] = useState(null);
  const [source, setSource] = useState(null);
  const [viewMode, setViewMode] = useState("weekly");
  const [dailyData, setDailyData] = useState([]);
  const [selectedWeek, setSelectedWeek] = useState(null);
  const [topAttendees, setTopAttendees] = useState([]);

  // Initial pie chart state
  const [pieChartData, setPieChartData] = useState({
    labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    datasets: [
      {
        data: [0, 0, 0, 0, 0, 0, 0],
        backgroundColor: [
          "#0099CC",
          "#FF5733",
          "#FF8D1A",
          "#FFB81C",
          "#F1D302",
          "#6BCB3C",
          "#A4E500",
        ],
        borderColor: "#ffffff",
        borderWidth: 1,
      },
    ],
  });

  // Load initial data on mount
  useEffect(() => {
    fetchAttendanceSummary();
    fetchTopAttendees();
  }, []);

  // Once attendance summary is loaded, fetch analytics data for the available date range
  useEffect(() => {
    if (attendanceSummarySet.size > 0) {
      const dates = Array.from(attendanceSummarySet).sort();
      const startDate = dates[0];
      const endDate = new Date().toISOString().split("T")[0];
      fetchAnalytics(startDate, endDate);
      fetchAttendanceByDayOfWeek(startDate, endDate);
    }
  }, [attendanceSummarySet]);

  /**
   * Fetch attendance summary from API.
   */
  const fetchAttendanceSummary = async () => {
    try {
      const res = await fetch("http://localhost:5000/admin/attendance_summary");
      const data = await res.json();
      if (data.success) {
        setAttendanceSummarySet(new Set(data.attendance_summary));
      }
    } catch (err) {
      console.error("Error fetching summary:", err);
    }
  };

  /**
   * Fetch detailed attendance records for a selected date.
   * @param {string} attendanceDate - Date string in YYYY-MM-DD format.
   */
  const fetchAttendanceDetails = async (attendanceDate) => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:5000/admin/attendance_records/${attendanceDate}`
      );
      const data = await response.json();
      if (data.success) {
        setAttendanceRecords(data.attendance_records);
        setSource(data.source);
        setDisclaimer(data.disclaimer);
      } else {
        setAttendanceRecords(null);
        setSource(null);
        setDisclaimer(null);
      }
    } catch (err) {
      console.error("Error fetching detailed attendance records:", err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Fetch analytics data within a date range.
   * @param {string} start - Start date in YYYY-MM-DD format.
   * @param {string} end - End date in YYYY-MM-DD format.
   */
  const fetchAnalytics = async (start, end) => {
    setAnalyticsLoading(true);
    try {
      const res = await fetch(
        `http://localhost:5000/admin/analytics/attendance?start_date=${start}&end_date=${end}`
      );
      const data = await res.json();
      if (data.success) {
        setAnalyticsData(data.analytics);
      }
    } catch (err) {
      console.error("Error fetching analytics:", err);
    } finally {
      setAnalyticsLoading(false);
    }
  };

  /**
   * Determines if a date should be highlighted on the calendar.
   * @param {object} param0 - Contains the date object.
   * @returns {string|null} - CSS class name if highlighted.
   */
  const highlightDates = ({ date }) => {
    const dateString = formatDate(date);
    return attendanceSummarySet.has(dateString) ? "highlight" : null;
  };

  /**
   * Handle click on a calendar date.
   * @param {Date} date - The clicked date object.
   */
  const handleDateClick = (date) => {
    const dateString = formatDate(date);
    if (attendanceSummarySet.has(dateString)) {
      setSelectedDate(dateString);
      fetchAttendanceDetails(dateString);
      setModalOpen(true);
    }
  };

  /**
   * Format a Date object to a YYYY-MM-DD string.
   * @param {Date} date - Date object.
   * @returns {string} - Formatted date string.
   */
  const formatDate = (date) => {
    const offset = date.getTimezoneOffset();
    const localDate = new Date(date.getTime() - offset * 60 * 1000);
    return localDate.toISOString().split("T")[0];
  };

  /**
   * Calculate start of the week from a given date.
   * @param {Date} date - Date object.
   * @returns {string} - Start of week in YYYY-MM-DD format.
   */
  const getStartOfWeek = (date) => {
    const d = new Date(date);
  const day = d.getDay(); 
  const diff = d.getDate() - day + (day === 0 ? -6 : 1); 
  return new Date(d.setDate(diff)).toISOString().split('T')[0];
  };

  /**
   * Group analytics data into weekly segments.
   * @param {Array} data - Array of analytics data.
   * @returns {Array} - Grouped weekly data.
   */
  const groupByWeek = (data) => {
    const grouped = {};
  
    data.forEach((entry) => {
      const date = new Date(entry.date);
      const weekStart = getStartOfWeek(date);
  
      if (!grouped[weekStart]) {
        grouped[weekStart] = {
          label: formatWeekLabel(weekStart),
          total: 0,
          days: [],
        };
      }
  
      grouped[weekStart].total += entry.total_attendance;
      grouped[weekStart].days.push(entry);
    });
  
    // Sort by weekStart and return last 5 weeks
    const sortedWeeks = Object.entries(grouped)
      .sort(([a], [b]) => new Date(a) - new Date(b))
      .slice(-5) // get last 5 weeks only
      .map(([, value]) => value);
  
    return sortedWeeks;
  };
  
  const formatWeekLabel = (startDateStr) => {
    const startDate = new Date(startDateStr);
    const endDate = new Date(startDate);
    endDate.setDate(startDate.getDate() + 6);
  
    const options = { month: "short", day: "numeric" };
    const startLabel = startDate.toLocaleDateString(undefined, options);
    const endLabel = endDate.toLocaleDateString(undefined, options);
  
    return `${startLabel} – ${endLabel}`;
  };

  // Prepare weekly grouped data for the line chart.
  const weeklyData = groupByWeek(analyticsData);

  /**
   * Handle click on a week segment of the line chart.
   * @param {Array} elements - Array of clicked chart elements.
   */
  const handleWeekClick = (elements) => {
    if (!elements.length) return;
    const index = elements[0].index;
    const selected = weeklyData[index];
    setDailyData(selected.days);
    setSelectedWeek(selected.label);
    setViewMode("daily");
  };

  // Prepare dynamic data for the line chart based on view mode.
  const lineChartData =
    viewMode === "weekly"
      ? {
          labels: weeklyData.map((w) => w.label),
          datasets: [
            {
              label: "Weekly Attendance",
              data: weeklyData.map((w) => w.total),
              borderColor: "rgba(16, 185, 129, 1)",
              fill: false,
              tension: 0.1,
            },
          ],
        }
      : {
          labels: dailyData.map((d) => d.date),
          datasets: [
            {
              label: `Attendance on ${selectedWeek}`,
              data: dailyData.map((d) => d.total_attendance),
              borderColor: "rgba(234, 88, 12, 1)",
              fill: false,
              tension: 0.1,
            },
          ],
        };

  /**
   * Fetch attendance data grouped by day of week for the pie chart.
   * @param {string} start - Start date in YYYY-MM-DD.
   * @param {string} end - End date in YYYY-MM-DD.
   */
  const fetchAttendanceByDayOfWeek = async (start, end) => {
    try {
      const res = await fetch(
        `http://localhost:5000/admin/attendance_by_day_of_week?start_date=${start}&end_date=${end}`
      );
      const data = await res.json();
      if (data.success) {
        const rawLabels = data.attendance_by_day.labels;
        const rawData = data.attendance_by_day.datasets[0].data;
        const rawColors = [
          "#f59e0b", 
          "#10b981", 
          "#ef4444", 
          "#8b5cf6", 
          "#22c55e", 
          "#e11d48", 
          "#11b8c6", 
        ];

        // Filter out entries where the attendance value is 0
        const filteredLabels = [];
        const filteredData = [];
        const filteredColors = [];
        rawLabels.forEach((label, index) => {
          if (rawData[index] !== 0) {
            filteredLabels.push(label);
            filteredData.push(rawData[index]);
            filteredColors.push(rawColors[index]);
          }
        });

        setPieChartData({
          labels: filteredLabels,
          datasets: [
            {
              data: filteredData,
              backgroundColor: filteredColors,
              borderColor: "#ffffff",
              borderWidth: 1,
            },
          ],
        });
      } else {
        console.error(
          "Error fetching attendance data by day of the week:",
          data.error
        );
      }
    } catch (err) {
      console.error("Error fetching attendance by day of the week:", err);
    }
  };

  /**
   * Fetch the top attendees from the server.
   */
  const fetchTopAttendees = async () => {
    try {
      const res = await fetch("http://localhost:5000/admin/top_attendees");
      const data = await res.json();
      if (data.success) {
        setTopAttendees(data.top_attendees);
      }
    } catch (err) {
      console.error("Error fetching top attendees:", err);
    }
  };

  // Data for the bar chart showcasing top attendees.
  const barChartData = {
    labels: topAttendees.map((user) => user.name),
    datasets: [
      {
        label: "Total Attendance",
        data: topAttendees.map((user) => user.total_attendance),
        backgroundColor: "rgba(132, 204, 22, 0.6)",
        borderColor: "rgba(132, 204, 22, 1)",
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className="admin-container">
      <Header title="Admin Dashboard" />
      <div className="dashboard-grid">
        {/* Calendar Cell */}
        <div className="dashboard-cell calendar-cell">
          <h3>Select a Date</h3>
          <Calendar
            tileClassName={highlightDates}
            onClickDay={handleDateClick}
            showNeighboringMonth={false}
          />
        </div>

        {/* Line Chart Cell */}
        <div className="dashboard-cell chart-cell">
          <h3>
            {viewMode === "weekly"
              ? "Weekly Attendance"
              : `Daily View - ${selectedWeek}`}
          </h3>
          {analyticsLoading ? (
            <p>Loading analytics...</p>
          ) : (
            <>
              <div className="chart-container">
                <Line
                  data={lineChartData}
                  options={{
                    onClick: (evt, elements) => {
                      if (viewMode === "weekly") handleWeekClick(elements);
                    },
                    plugins: {
                      legend: {
                        position: "bottom",
                      },
                    },
                  }}
                />
              </div>
              {viewMode === "daily" && (
                <button
                  className="back-button"
                  onClick={() => setViewMode("weekly")}
                >
                  ⬅ Back to Weekly View
                </button>
              )}
            </>
          )}
        </div>

        {/* Pie Chart Cell */}
        <div className="dashboard-cell chart-cell pie-chart">
          <h3>Attendance Breakdown</h3>
          {analyticsLoading ? (
            <p>Loading analytics...</p>
          ) : (
            <div className="chart-container">
              <Pie
                data={pieChartData}
                options={{
                  maintainAspectRatio: false,
                  responsive: true,
                  plugins: {
                    legend: {
                      display: false,
                    },
                    datalabels: {
                      color: "#fff",
                      font: {
                        weight: "bold",
                        size: 14,
                      },
                      formatter: (value, context) =>
                        context.chart.data.labels[context.dataIndex],
                    },
                  },
                }}
              />
            </div>
          )}
        </div>

        {/* Bar Chart Cell */}
        <div className="dashboard-cell chart-cell">
          <h3>Top 5 Users With Highest Attendance</h3>
          {topAttendees.length === 0 ? (
            <p>Loading top attendees...</p>
          ) : (
            <div className="chart-container">
              <Bar
                data={barChartData}
                options={{
                  plugins: {
                    legend: {
                      position: "bottom",
                    },
                  },
                  onClick: (evt, elements) => {
                    if (!elements.length) return;
                    const index = elements[0].index;
                    const selectedUser = topAttendees[index];
                    if (selectedUser && selectedUser.name) {
                      window.location.href = `/attendance-records?name=${encodeURIComponent(selectedUser.name)}`;
                    }
                  },
                  
                }}
              />
            </div>
          )}
        </div>
      </div>

      {/* Modal for Detailed Attendance */}
      {modalOpen && selectedDate && (
        <div className="modal" onClick={() => setModalOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <span className="close" onClick={() => setModalOpen(false)}>
              &times;
            </span>
            <h3>Attendance for {selectedDate}</h3>
            <div className="modal-body">
              {loading ? (
                <p>Loading records...</p>
              ) : (
                <AdminAttendanceTable records={attendanceRecords} />
              )}
              {source === "postgres" && disclaimer && (
                <p className="disclaimer">{disclaimer}</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
