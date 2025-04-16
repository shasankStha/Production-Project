import React, { useEffect, useState } from "react";
import axios from "axios";
import UserTable from "../components/UserTable";
import EditUserModal from "../components/EditUserModal";
import { getToken } from "../utils/Auth";
import "../styles/UserManagement.css";
import Sidebar from "../components/Sidebar";

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [editingUser, setEditingUser] = useState(null);

  const fetchUsers = async () => {
    try {
      const token = getToken();
      const res = await axios.get("http://localhost:5000/admin/users", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUsers(res.data.users);
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

  return (
    <div className="dashboard-container">
      <Sidebar />
      <div className="main-content">
        <h1 className="text-2xl font-bold mb-4">User Management</h1>
        <UserTable users={users} onEdit={handleEdit} onDelete={handleDelete} />
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
