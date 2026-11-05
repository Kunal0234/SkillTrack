import { Routes, Route, Navigate } from "react-router-dom";

import Sidebar from "./components/Sidebar.jsx";
import Navbar from "./components/Navbar.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";

import "./App.css";

function Dashboard() {
  const stats = [
    {
      title: "Enrolled Courses",
      value: "04",
      description: "Courses you're learning",
    },
    {
      title: "Completed Lessons",
      value: "12",
      description: "Lessons completed so far",
    },
    {
      title: "Learning Progress",
      value: "65%",
      description: "Overall progress",
    },
  ];

  return (
    <div className="app-layout">
      <Sidebar />

      <main className="main-content">
        <Navbar />

        <section className="dashboard-content">
          <div className="welcome-section">
            <h1>Welcome back, Student! 👋</h1>
            <p>Keep learning. Every lesson brings you closer to your goals.</p>
          </div>

          <div className="stats-grid">
            {stats.map((stat) => (
              <div className="stat-card" key={stat.title}>
                <p>{stat.title}</p>
                <h2>{stat.value}</h2>
                <span>{stat.description}</span>
              </div>
            ))}
          </div>

          <div className="learning-section">
            <h2>Continue Learning</h2>

            <div className="course-card">
              <div>
                <h3>Python Full Stack Development</h3>
                <p>Keep going! You're making progress.</p>
              </div>

              <span className="progress-label">65% completed</span>

              <div className="progress-bar">
                <div className="progress-fill"></div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dashboard" element={<Dashboard />} />

      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}

export default App;
