function Sidebar() {
  return (
    <aside className="sidebar">
      <h2 className="logo">SkillTrack</h2>

      <nav className="sidebar-nav">
        <a href="/" className="active">
          Dashboard
        </a>
        <a href="/courses">Explore Courses</a>
        <a href="/learning">My Learning</a>
        <a href="/progress">My Progress</a>
        <a href="/profile">Profile</a>
      </nav>

      <button className="logout-btn">Logout</button>
    </aside>
  );
}

export default Sidebar;
