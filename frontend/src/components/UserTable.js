import React from "react";

const UserTable = ({ users, onEdit, onDelete }) => {
  return (
    <table className="user-table">
      <thead>
        <tr>
          <th>S.N.</th>
          <th>Name</th>
          <th>Username</th>
          <th>Email</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {users.map((user, index) => (
          <tr key={user.user_id}>
            <td>{index + 1}</td>
            <td>
              {user.first_name} {user.last_name}
            </td>
            <td>{user.username}</td>
            <td>{user.email}</td>
            <td>
              <button className="edit-btn" onClick={() => onEdit(user)}>
                Edit
              </button>
              <button
                className="delete-btn"
                onClick={() => onDelete(user.user_id)}
              >
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default UserTable;
