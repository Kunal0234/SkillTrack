function Navbar({ userName, role }) {
  return (
    <header className="navbar">
      <div>
        <h2>SkillTrack</h2>
        <p>Welcome back! Continue your journey.</p>
      </div>

      <div className="navbar-user">
        <div>
          <span>{userName}</span>
          <p>{role}</p>
        </div>

        <div className="user-avatar">{userName.charAt(0).toUpperCase()}</div>
      </div>
    </header>
  );
}

export default Navbar;
