import { useEffect, useState } from "react";
import DashboardLayout from "../components/DashboardLayout.jsx";
import { getInstructorCourses } from "../services/api.js";

const InstructorCourses = () => {
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
          <h1>My Courses</h1>
          <p>Manage all the courses created by you.</p>
        </div>

        {loading && <p>Loading courses...</p>}
        {error && <p className="error-message">{error}</p>}

        {!loading && !error && courses.length === 0 && (
          <p>You haven't created any courses yet.</p>
        )}

        {!loading && !error && courses.length > 0 && (
          <div className="courses-grid">
            {courses.map((course) => (
              <div className="course-card" key={course.id}>
                <h3>{course.title}</h3>
                <p>{course.description}</p>
                <span>Course ID: {course.id}</span>
              </div>
            ))}
          </div>
        )}
      </section>
    </DashboardLayout>
  );
};

export default InstructorCourses;
