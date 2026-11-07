import DashboardLayout from "../components/DashboardLayout.jsx";

const AdminDashboard = () => {
  return (
    <DashboardLayout>
      <section className="dashboard-content">
        <div className="welcome-section">
          <h1>Admin Dashboard</h1>
          <p>Manage users and instructor applications.</p>
        </div>
      </section>
    </DashboardLayout>
  );
};

export default AdminDashboard;
