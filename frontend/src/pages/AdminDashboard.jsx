
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import DashboardLayout from "../components/DashboardLayout.jsx";
import StatCard from "../components/StatCard.jsx";
import { getInstructorApplications } from "../services/api.js";

const AdminDashboard = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchApplications = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const data = await getInstructorApplications(token);
        setApplications(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchApplications();
  }, []);

  return (
    <DashboardLayout>
      <section className="dashboard-content">
        <div className="welcome-section">
          <h1>Admin Dashboard</h1>
          <p>Manage users and instructor applications.</p>
        </div>

        <div className="stats-container">
          <StatCard
            title="Pending Applications"
            value={loading ? "..." : applications.length}
            description="Applications waiting for review"
          />
        </div>

        {error && <p className="error-message">{error}</p>}

        <div className="courses-section">
          <h2>Instructor Applications</h2>
          <p>Review requests from users who want to become instructors.</p>

          <Link to="/admin/applications" className="admin-action-btn">
            Manage Applications
          </Link>
        </div>
      </section>
    </DashboardLayout>
  );
};

export default AdminDashboard;
