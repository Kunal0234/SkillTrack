import { useEffect, useState } from "react";
import DashboardLayout from "../components/DashboardLayout.jsx";
import StatCard from "../components/StatCard.jsx";
import {
  getMyEnrollments,
  getMyProgress,
  getCourses,
} from "../services/api.js";

const StudentDashboard = () => {
  const [enrollments, setEnrollments] = useState([]);
  const [progress, setProgress] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const token = localStorage.getItem("access_token");

        const [enrollmentData, progressData, courseData] = await Promise.all([
          getMyEnrollments(token),
          getMyProgress(token),
          getCourses(),
        ]);

        setEnrollments(enrollmentData);
        setProgress(progressData);
        setCourses(courseData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const enrolledCourses = enrollments
    .map((enrollment) =>
      courses.find((course) => course.id === enrollment.course_id),
    )
    .filter(Boolean);

  return (
    <DashboardLayout>
      <section className="dashboard-content">
        <div className="welcome-section">
          <h1>Student Dashboard</h1>
          <p>Welcome! Continue your learning journey.</p>
        </div>

        {loading && <p>Loading dashboard...</p>}
        {error && <p>{error}</p>}

        {!loading && !error && (
          <>
            <div className="stats-container">
              <StatCard
                title="Enrolled Courses"
                value={enrollments.length}
                description="Courses you're learning"
              />

              <StatCard
                title="Completed Lessons"
                value={progress.length}
                description="Lessons completed"
              />
            </div>

            <div className="courses-section">
              <h2>My Courses</h2>

              {enrolledCourses.length === 0 ? (
                <p>You haven't enrolled in any courses yet.</p>
              ) : (
                <div className="courses-grid">
                  {enrolledCourses.map((course) => (
                    <div className="course-card" key={course.id}>
                      <h3>{course.title}</h3>
                      <p>{course.description}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </section>
    </DashboardLayout>
  );
};

export default StudentDashboard;
