import Sidebar from "./components/Sidebar.jsx";
import Navbar from "./components/Navbar.jsx";
import "./App.css";

function App() {
  return (
    <div className="app-layout">
      <Sidebar />

      <main className="main-content">
        <Navbar />

        <section className="dashboard-content">
          <h1>Welcome to SkillTrack</h1>
          <p>Your learning journey starts here.</p>
        </section>
      </main>
    </div>
  );
}

export default App;
