import React from "react";
import "../styles/UserManagement.css";

const DeleteConfirmationModal = ({ user, onConfirm, onCancel }) => {
    console.log(user)
    return (
      <div className="edit-modal">
        <div className="edit-modal-content">
          <h2 className="modal-title">Confirm Deletion</h2>
          <p>
            Are you sure you want to delete?
          </p>
          <div className="modal-actions">
            <button className="save-btn" onClick={() => onConfirm(user)}>
              Yes
            </button>
            <button className="cancel-btn" onClick={onCancel}>
              No
            </button>
          </div>
        </div>
      </div>
    );
  };
  
  export default DeleteConfirmationModal;