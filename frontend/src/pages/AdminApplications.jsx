import { useEffect, useState } from "react";
import DashboardLayout from "../components/DashboardLayout.jsx";
import {
  getInstructorApplications,
  reviewInstructorApplication,
} from "../services/api.js";

const AdminApplications = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processingId, setProcessingId] = useState(null);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

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

  useEffect(() => {
    const loadApplications = async () => {
      await fetchApplications();
    };

    loadApplications();
  }, []);
  const handleReview = async (applicationId, status) => {
    try {
      setProcessingId(applicationId);
      setError("");
      setMessage("");

      const token = localStorage.getItem("access_token");

      await reviewInstructorApplication(applicationId, status, token);

      setApplications((previous) =>
        previous.filter((app) => app.id !== applicationId),
      );

      setMessage(`Application ${status} successfully!`);
    } catch (err) {
      setError(err.message);
    } finally {
      setProcessingId(null);
    }
  };

  return (
    <DashboardLayout>
      <section className="dashboard-content">
        <div className="welcome-section">
          <h1>Instructor Applications</h1>
          <p>Review and manage instructor applications.</p>
        </div>

        {loading && <p>Loading applications...</p>}

        {error && <p className="error-message">{error}</p>}

        {message && <p className="success-message">{message}</p>}

        {!loading && applications.length === 0 && (
          <p>No pending applications available.</p>
        )}

        {!loading && applications.length > 0 && (
          <div className="courses-grid">
            {applications.map((application) => (
              <div className="course-card" key={application.id}>
                <h3>Application #{application.id}</h3>

                <p>
                  <strong>User ID:</strong> {application.user_id}
                </p>

                <p>
                  <strong>Submitted:</strong>{" "}
                  {new Date(application.created_at).toLocaleDateString()}
                </p>

                <p>
                  <strong>Reason:</strong>
                </p>

                <p>{application.reason}</p>

                <div className="application-actions">
                  <button
                    className="approve-btn"
                    disabled={processingId !== null}
                    onClick={() => handleReview(application.id, "approved")}
                  >
                    {processingId === application.id
                      ? "Processing..."
                      : "Approve"}
                  </button>

                  <button
                    className="reject-btn"
                    disabled={processingId !== null}
                    onClick={() => handleReview(application.id, "rejected")}
                  >
                    {processingId === application.id
                      ? "Processing..."
                      : "Reject"}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </DashboardLayout>
  );
};

export default AdminApplications;
