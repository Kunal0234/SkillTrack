import DashboardLayout from "../components/DashboardLayout.jsx";

const InstructorDashboard = () => {
  const courses = [
    {
      id: 1,
      title: "Python Full Stack Development",
      students: 25,
      lessons: 12,
    },
    {
      id: 2,
      title: "Generative AI Fundamentals",
      students: 18,
      lessons: 8,
    },
  ];

  return (
    <DashboardLayout>
      <section className="dashboard-content">
        <div className="welcome-section">
          <h1>Instructor Dashboard</h1>
          <p>Manage your courses and help students learn.</p>
        </div>

        <div className="stats-container">
          <div className="stat-card">
            <h3>Total Courses</h3>
            <h2>{courses.length}</h2>
          </div>

          <div className="stat-card">
            <h3>Total Students</h3>
            <h2>
              {courses.reduce((total, course) => total + course.students, 0)}
            </h2>
          </div>
        </div>

        <div className="courses-section">
          <h2>My Courses</h2>

          <div className="courses-grid">
            {courses.map((course) => (
              <div className="course-card" key={course.id}>
                <h3>{course.title}</h3>
                <p>{course.students} Students</p>
                <p>{course.lessons} Lessons</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </DashboardLayout>
  );
};

export default InstructorDashboard;
