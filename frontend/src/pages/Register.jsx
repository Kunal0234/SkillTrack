import { Link } from "react-router-dom";

const Register = () => {
  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>Create Account</h1>
        <p>Join SkillTrack and start learning.</p>

        <form>
          <label htmlFor="name">Full Name</label>
          <input id="name" type="text" placeholder="Enter your name" required />

          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            placeholder="Enter your email"
            required
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            placeholder="Create a password"
            required
          />

          <label htmlFor="role">Account Type</label>
          <select id="role" defaultValue="student">
            <option value="student">Student</option>
            <option value="instructor">Instructor</option>
          </select>

          <button type="submit">Create Account</button>
        </form>

        <p>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
