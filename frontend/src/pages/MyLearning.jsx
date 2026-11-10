
import { useEffect, useState } from "react";
import DashboardLayout from "../components/DashboardLayout.jsx";
import { getMyEnrollments, getCourses } from "../services/api.js";

const MyLearning = () => {
  const [myCourses, setMyCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchMyLearning = async () => {
      try {
        const token = localStorage.getItem("access_token");

        const [enrollments, courses] = await Promise.all([
          getMyEnrollments(token),
          getCourses(),
        ]);

        const enrolledCourses = enrollments
          .map((enrollment) =>
            courses.find((course) => course.id === enrollment.course_id)
          )
          .filter(Boolean);

        setMyCourses(enrolledCourses);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchMyLearning();
  }, []);

  return (
    <DashboardLayout>
      <section className="dashboard-content">
        <div className="welcome-section">
          <h1>My Learning</h1>
          <p>Continue learning from your enrolled courses.</p>
        </div>

        {loading && <p>Loading your courses...</p>}
        {error && <p>{error}</p>}

        {!loading && !error && myCourses.length === 0 && (
          <p>You haven't enrolled in any courses yet.</p>
        )}

        {!loading && !error && myCourses.length > 0 && (
          <div className="courses-grid">
            {myCourses.map((course) => (
              <div className="course-card" key={course.id}>
                <h3>{course.title}</h3>
                <p>{course.description}</p>
                <span className="progress-label">Enrolled</span>
              </div>
            ))}
          </div>
        )}
      </section>
    </DashboardLayout>
  );
};

export default MyLearning;
