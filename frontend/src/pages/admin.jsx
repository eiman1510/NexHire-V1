import { useState, useEffect } from "react";
import * as api from "../services/api";
import "../styles/admin.css";

export default function AdminDashboard() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [password, setPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("approved");
  const [approvedHRs, setApprovedHRs] = useState([]);
  const [registeredHRs, setRegisteredHRs] = useState([]);
  const [newHREmail, setNewHREmail] = useState("");
  const [dataLoading, setDataLoading] = useState(false);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const handlePasswordLogin = async (e) => {
    e.preventDefault();
    setPasswordError("");
    setLoading(true);

    try {
      await api.adminLogin(password);
      setIsAuthenticated(true);
      setPassword("");
      loadDashboardData();
    } catch (err) {
      setPasswordError(
        err.message || "Invalid password. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const loadDashboardData = async () => {
    setDataLoading(true);
    try {
      const [approved, registered] = await Promise.all([
        api.getApprovedHRs(),
        api.getRegisteredHRs(),
      ]);
      setApprovedHRs(approved);
      setRegisteredHRs(registered);
      setError("");
    } catch (err) {
      setError("Failed to load dashboard data");
    } finally {
      setDataLoading(false);
    }
  };

  const handleAddHR = async (e) => {
    e.preventDefault();
    if (!newHREmail.trim()) {
      setError("Please enter an email address");
      return;
    }

    setDataLoading(true);
    try {
      await api.addHR(newHREmail);
      setSuccessMessage(`HR added successfully: ${newHREmail}`);
      setNewHREmail("");
      loadDashboardData();
      setTimeout(() => setSuccessMessage(""), 3000);
    } catch (err) {
      setError(err.message || "Failed to add HR");
    } finally {
      setDataLoading(false);
    }
  };

  const handleDeleteHR = async (email) => {
    if (!window.confirm(`Are you sure you want to remove ${email} as HR?`)) {
      return;
    }

    setDataLoading(true);
    try {
      await api.deleteHR(email);
      setSuccessMessage(`HR removed successfully: ${email}`);
      loadDashboardData();
      setTimeout(() => setSuccessMessage(""), 3000);
    } catch (err) {
      setError(err.message || "Failed to remove HR");
    } finally {
      setDataLoading(false);
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setPassword("");
    setNewHREmail("");
    setApprovedHRs([]);
    setRegisteredHRs([]);
    setActiveTab("approved");
  };

  // Password Screen
  if (!isAuthenticated) {
    return (
      <div className="admin-password-screen">
        <div className="password-container">
          <h1>Admin Dashboard</h1>
          <p className="subtitle">Enter Password to Access</p>
          <form onSubmit={handlePasswordLogin} className="password-form">
            <div className="form-group">
              <input
                type="password"
                placeholder="Enter admin password"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  setPasswordError("");
                }}
                disabled={loading}
                className={passwordError ? "input-error" : ""}
              />
            </div>
            {passwordError && (
              <p className="error-message">{passwordError}</p>
            )}
            <button type="submit" disabled={loading}>
              {loading ? "Authenticating..." : "Login"}
            </button>
          </form>
        </div>
      </div>
    );
  }

  // Admin Dashboard
  return (
    <div className="admin-dashboard">
      <header className="admin-header">
        <div className="header-content">
          <h1>Admin Dashboard</h1>
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <main className="admin-main">
        {/* Add HR Section */}
        <section className="add-hr-section">
          <h2>Add HR</h2>
          <form onSubmit={handleAddHR} className="add-hr-form">
            <input
              type="email"
              placeholder="Enter HR email address"
              value={newHREmail}
              onChange={(e) => {
                setNewHREmail(e.target.value);
                setError("");
              }}
              disabled={dataLoading}
              className="email-input"
            />
            <button type="submit" disabled={dataLoading} className="add-btn">
              {dataLoading ? "Adding..." : "+ Add HR"}
            </button>
          </form>
        </section>

        {/* Messages */}
        {successMessage && (
          <div className="success-message">{successMessage}</div>
        )}
        {error && <div className="error-message-banner">{error}</div>}

        {/* Tabs */}
        <div className="tabs-container">
          <button
            className={`tab ${activeTab === "approved" ? "active" : ""}`}
            onClick={() => setActiveTab("approved")}
          >
            Approved HRs
          </button>
          <button
            className={`tab ${activeTab === "registered" ? "active" : ""}`}
            onClick={() => setActiveTab("registered")}
          >
            Registered Users
          </button>
        </div>

        {/* Table */}
        <div className="table-container">
          {dataLoading && <p className="loading">Loading...</p>}
          {!dataLoading && (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Email</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {activeTab === "approved" &&
                  approvedHRs.map((hr, index) => (
                    <tr key={index}>
                      <td>{hr.email || hr}</td>
                      <td>
                        <button
                          className="delete-btn"
                          onClick={() => handleDeleteHR(hr.email || hr)}
                          title="Delete HR"
                        >
                          🗑
                        </button>
                      </td>
                    </tr>
                  ))}
                {activeTab === "registered" &&
                  registeredHRs.map((user, index) => (
                    <tr key={index}>
                      <td>{user.email || user}</td>
                      <td>
                        <button
                          className="delete-btn"
                          onClick={() => handleDeleteHR(user.email || user)}
                          title="Delete User"
                        >
                          🗑
                        </button>
                      </td>
                    </tr>
                  ))}
                {activeTab === "approved" && approvedHRs.length === 0 && (
                  <tr>
                    <td colSpan="2" className="empty-state">
                      No approved HRs found
                    </td>
                  </tr>
                )}
                {activeTab === "registered" && registeredHRs.length === 0 && (
                  <tr>
                    <td colSpan="2" className="empty-state">
                      No registered users found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      </main>
    </div>
  );
}
