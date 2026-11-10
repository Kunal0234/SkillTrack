import { useState } from "react";
import DashboardLayout from "../components/DashboardLayout.jsx";
import { createCourse } from "../services/api.js";

const CreateCourse = () => {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleChange = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      const token = localStorage.getItem("access_token");
      await createCourse(formData, token);

      setMessage("Course created successfully!");
      setFormData({ title: "", description: "" });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <section className="dashboard-content">
        <div className="welcome-section">
          <h1>Create Course</h1>
          <p>Add a new course for students.</p>
        </div>

        <form className="create-course-form" onSubmit={handleSubmit}>
          <label>Course Title</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="Enter course title"
            minLength={3}
            maxLength={200}
            required
          />

          <label>Course Description</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Describe your course"
            rows={5}
          />

          <button type="submit" disabled={loading}>
            {loading ? "Creating..." : "Create Course"}
          </button>

          {error && <p className="error-message">{error}</p>}
          {message && <p className="success-message">{message}</p>}
        </form>
      </section>
    </DashboardLayout>
  );
};

export default CreateCourse;
