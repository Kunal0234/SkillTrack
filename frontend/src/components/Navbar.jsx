function Navbar({ userName, onLogout }) {
  return (
    <header className="navbar">
      <div>
        <h2>Dashboard</h2>
        <p>Welcome back! Continue your learning journey.</p>
      </div>

      <div className="navbar-user">
        <span>{userName}</span>
        <div className="user-avatar">{userName.charAt(0).toUpperCase()}</div>

        <button onClick={onLogout} className="logout-btn">
          Logout
        </button>
      </div>
    </header>
  );
}

export default Navbar;
