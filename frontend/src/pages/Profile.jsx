import DashboardLayout from "../components/DashboardLayout.jsx";

const Profile = () => {
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  return (
    <DashboardLayout>
      <section className="dashboard-content">
        <div className="welcome-section">
          <h1>My Profile</h1>
          <p>View your account information.</p>
        </div>

        <div className="course-card profile-card">
          <h3>Personal Information</h3>

          <p><strong>Name:</strong> {user.name || "N/A"}</p>
          <p><strong>Email:</strong> {user.email || "N/A"}</p>
          <p><strong>Role:</strong> {user.role || "N/A"}</p>
        </div>
      </section>
    </DashboardLayout>
  );
};

export default Profile;