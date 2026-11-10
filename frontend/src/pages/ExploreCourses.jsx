import { useEffect, useState } from "react";
import DashboardLayout from "../components/DashboardLayout.jsx";
import {
  getCourses,
  getMyEnrollments,
  enrollInCourse,
} from "../services/api.js";

const ExploreCourses = () => {
  const [courses, setCourses] = useState([]);
  const [enrollments, setEnrollments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadingCourseId, setLoadingCourseId] = useState(null);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("access_token");

        const [courseData, enrollmentData] = await Promise.all([
          getCourses(),
          getMyEnrollments(token),
        ]);

        setCourses(courseData);
        setEnrollments(enrollmentData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleEnroll = async (courseId) => {
    try {
      setLoadingCourseId(courseId);
      setError("");
      setMessage("");

      const token = localStorage.getItem("access_token");
      const newEnrollment = await enrollInCourse(courseId, token);

      setEnrollments((previous) => [...previous, newEnrollment]);
      setMessage("Successfully enrolled in the course!");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingCourseId(null);
    }
  };

  const enrolledCourseIds = enrollments.map(
    (enrollment) => enrollment.course_id,
  );

  return (
    <DashboardLayout>
      <section className="dashboard-content">
        <div className="welcome-section">
          <h1>Explore Courses</h1>
          <p>Discover courses and start learning something new.</p>
        </div>

        {loading && <p>Loading courses...</p>}
        {error && <p>{error}</p>}
        {message && <p>{message}</p>}

        {!loading && courses.length === 0 && (
          <p>No courses are available right now.</p>
        )}

        {!loading && (
          <div className="courses-grid">
            {courses.map((course) => {
              const isEnrolled = enrolledCourseIds.includes(course.id);

              return (
                <div className="course-card" key={course.id}>
                  <h3>{course.title}</h3>
                  <p>{course.description}</p>

                  <button
                    className="enroll-btn"
                    disabled={isEnrolled || loadingCourseId === course.id}
                    onClick={() => handleEnroll(course.id)}
                  >
                    {isEnrolled
                      ? "Enrolled"
                      : loadingCourseId === course.id
                        ? "Enrolling..."
                        : "Enroll Now"}
                  </button>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </DashboardLayout>
  );
};

export default ExploreCourses;
