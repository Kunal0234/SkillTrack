import { Link } from "react-router-dom";

function Sidebar({ role, onLogout }) {
  const navigation = {
    student: [{ label: "Dashboard", path: "/student" }],

    instructor: [{ label: "Dashboard", path: "/instructor" }],

    admin: [{ label: "Dashboard", path: "/admin" }],
  };

  const links = navigation[role] || [];

  return (
    <aside className="sidebar">
      <h2 className="logo">SkillTrack</h2>

      <nav className="sidebar-nav">
        {links.map((item) => (
          <Link key={item.path} to={item.path}>
            {item.label}
          </Link>
        ))}
      </nav>

      <button className="logout-btn" onClick={onLogout}>
        Logout
      </button>
    </aside>
  );
}

export default Sidebar;
