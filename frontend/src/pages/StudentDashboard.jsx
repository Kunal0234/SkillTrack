import DashboardLayout from "../components/DashboardLayout.jsx";

const StudentDashboard = () => {
  return (
    <DashboardLayout>
      <section className="dashboard-content">
        <div className="welcome-section">
          <h1>Student Dashboard</h1>
          <p>Welcome! Continue your learning journey.</p>
        </div>
      </section>
    </DashboardLayout>
  );
};

export default StudentDashboard;