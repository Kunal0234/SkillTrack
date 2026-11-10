
import { Link } from "react-router-dom";

function Sidebar({ role, onLogout }) {
  const navigation = {
    student: [
      { label: "Dashboard", path: "/student" },
      { label: "Explore Courses", path: "/student/explore" },
      { label: "My Learning", path: "/student/learning" },
      { label: "My Progress", path: "/student/progress" },
      { label: "Profile", path: "/student/profile" },
    ],

    instructor: [
      { label: "Dashboard", path: "/instructor" },
      { label: "My Courses", path: "/instructor/courses" },
      { label: "Create Course", path: "/instructor/courses/create" },
    ],

    admin: [
      { label: "Dashboard", path: "/admin" },
      { label: "Users", path: "/admin/users" },
      { label: "Applications", path: "/admin/applications" },
    ],
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
