import { useNavigate } from "react-router-dom";
import Sidebar from "./Sidebar.jsx";
import Navbar from "./Navbar.jsx";

function DashboardLayout({ children }) {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <div className="app-layout">
      <Sidebar role={user.role} onLogout={handleLogout} />

      <main className="main-content">
        <Navbar userName={user.name || "User"} role={user.role} />

        {children}
      </main>
    </div>
  );
}

export default DashboardLayout;
