import React, { useEffect, useState } from "react";
import axios from "axios";
import UserTable from "../components/UserTable";
import EditUserModal from "../components/EditUserModal";
import { getToken } from "../utils/Auth";
import "../styles/UserManagement.css";
import Header from "../components/Header";

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [editingUser, setEditingUser] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const USERS_PER_PAGE = 8;

  const fetchUsers = async () => {
    try {
      const token = getToken();
      const res = await axios.get("http://localhost:5000/admin/users", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const sortedUsers = res.data.users.sort((a, b) =>
        a.first_name.localeCompare(b.first_name)
      );
      setUsers(sortedUsers);
    } catch (error) {
      console.error("Failed to fetch users", error);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleDelete = async (id) => {
    const confirm = window.confirm("Are you sure you want to delete this user?");
    if (!confirm) return;
    try {
      const token = getToken();
      await axios.delete(`http://localhost:5000/admin/users/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchUsers();
    } catch (error) {
      console.error("Error deleting user", error);
    }
  };

  const handleEdit = (user) => {
    setEditingUser(user);
  };

  const handleUpdate = async (updatedUser) => {
    try {
      const token = getToken();
      await axios.put(`http://localhost:5000/admin/users/${updatedUser.user_id}`, updatedUser, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setEditingUser(null);
      fetchUsers();
    } catch (error) {
      console.error("Error updating user", error);
      if (error.response?.data?.message) {
        alert(error.response.data.message);
      } else {
        alert("Failed to update user. Try again.");
      }
    }
  };

  // Pagination logic
  const totalPages = Math.ceil(users.length / USERS_PER_PAGE);
  const paginatedUsers = users.slice(
    (currentPage - 1) * USERS_PER_PAGE,
    currentPage * USERS_PER_PAGE
  );

  const goToPage = (page) => {
    if (page >= 1 && page <= totalPages) setCurrentPage(page);
  };

  return (
    <div className="dashboard-container">
      <Header title="Manage User" />
      <div className="main-content">
        <UserTable users={paginatedUsers} onEdit={handleEdit} onDelete={handleDelete} />
        
        {/* Pagination Controls */}
        <div className="pagination-controls">
          <button onClick={() => goToPage(currentPage - 1)} disabled={currentPage === 1}>
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
          <button onClick={() => goToPage(currentPage + 1)} disabled={currentPage === totalPages}>
            Next
          </button>
        </div>

        {editingUser && (
          <EditUserModal
            user={editingUser}
            onClose={() => setEditingUser(null)}
            onSave={handleUpdate}
          />
        )}
      </div>
    </div>
  );
};

export default UserManagement;
