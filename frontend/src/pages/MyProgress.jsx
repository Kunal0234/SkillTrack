import { useEffect, useState } from "react";
import DashboardLayout from "../components/DashboardLayout.jsx";
import { getMyProgress } from "../services/api.js";

const MyProgress = () => {
  const [progress, setProgress] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProgress = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const data = await getMyProgress(token);
        setProgress(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProgress();
  }, []);

  return (
    <DashboardLayout>
      <section className="dashboard-content">
        <div className="welcome-section">
          <h1>My Progress</h1>
          <p>Track your learning progress here.</p>
        </div>

        {loading && <p>Loading progress...</p>}
        {error && <p>{error}</p>}

        {!loading && !error && (
          <div className="courses-section">
            <h2>Completed Lessons</h2>

            {progress.length === 0 ? (
              <p>You haven't completed any lessons yet.</p>
            ) : (
              <div className="courses-grid">
                {progress.map((item) => (
                  <div className="course-card" key={item.id}>
                    <h3>Lesson ID: {item.lesson_id}</h3>
                    <p>Status: Completed</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </section>
    </DashboardLayout>
  );
};

export default MyProgress;
