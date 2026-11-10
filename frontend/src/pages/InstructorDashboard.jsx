
import { useEffect, useState } from "react";
import DashboardLayout from "../components/DashboardLayout.jsx";
import StatCard from "../components/StatCard.jsx";
import { getInstructorCourses } from "../services/api.js";

const InstructorDashboard = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const data = await getInstructorCourses(token);
        setCourses(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  return (
    <DashboardLayout>
      <section className="dashboard-content">
        <div className="welcome-section">
          <h1>Instructor Dashboard</h1>
          <p>Manage your courses and help students learn.</p>
        </div>

        <div className="stats-container">
          <StatCard
            title="Total Courses"
            value={courses.length}
            description="Courses created by you"
          />
        </div>

        <div className="courses-section">
          <h2>My Courses</h2>

          {loading && <p>Loading courses...</p>}
          {error && <p>{error}</p>}

          {!loading && !error && courses.length === 0 && (
            <p>You haven't created any courses yet.</p>
          )}

          {!loading && !error && (
            <div className="courses-grid">
              {courses.map((course) => (
                <div className="course-card" key={course.id}>
                  <h3>{course.title}</h3>
                  <p>{course.description}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </DashboardLayout>
  );
};

export default InstructorDashboard;
