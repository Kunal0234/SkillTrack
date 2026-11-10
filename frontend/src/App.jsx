import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";

import ProtectedRoute from "./components/ProtectedRoute.jsx";

import StudentDashboard from "./pages/StudentDashboard.jsx";
import InstructorDashboard from "./pages/InstructorDashboard.jsx";
import AdminDashboard from "./pages/AdminDashboard.jsx";

import ExploreCourses from "./pages/ExploreCourses.jsx";
import MyLearning from "./pages/MyLearning.jsx";
import MyProgress from "./pages/MyProgress.jsx";
import Profile from "./pages/Profile.jsx";

import CreateCourse from "./pages/CreateCourse.jsx";
import InstructorCourses from "./pages/InstructorCourses.jsx";

import "./App.css";

function RoleRoute({ allowedRole, children }) {
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  if (user.role !== allowedRole) {
    const paths = {
      student: "/student",
      instructor: "/instructor",
      admin: "/admin",
    };

    return <Navigate to={paths[user.role] || "/login"} replace />;
  }

  return children;
}

function App() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Protected Routes */}
      <Route element={<ProtectedRoute />}>
        {/* Student Routes */}
        <Route
          path="/student"
          element={
            <RoleRoute allowedRole="student">
              <StudentDashboard />
            </RoleRoute>
          }
        />

        <Route
          path="/student/explore"
          element={
            <RoleRoute allowedRole="student">
              <ExploreCourses />
            </RoleRoute>
          }
        />

        <Route
          path="/student/learning"
          element={
            <RoleRoute allowedRole="student">
              <MyLearning />
            </RoleRoute>
          }
        />

        <Route
          path="/student/progress"
          element={
            <RoleRoute allowedRole="student">
              <MyProgress />
            </RoleRoute>
          }
        />

        <Route
          path="/student/profile"
          element={
            <RoleRoute allowedRole="student">
              <Profile />
            </RoleRoute>
          }
        />

        {/* Instructor Routes */}
        <Route
          path="/instructor"
          element={
            <RoleRoute allowedRole="instructor">
              <InstructorDashboard />
            </RoleRoute>
          }
        />

        <Route
          path="/instructor/courses"
          element={
            <RoleRoute allowedRole="instructor">
              <InstructorCourses />
            </RoleRoute>
          }
        />

        <Route
          path="/instructor/courses/create"
          element={
            <RoleRoute allowedRole="instructor">
              <CreateCourse />
            </RoleRoute>
          }
        />

        {/* Admin Route */}
        <Route
          path="/admin"
          element={
            <RoleRoute allowedRole="admin">
              <AdminDashboard />
            </RoleRoute>
          }
        />
      </Route>

      {/* Default Routes */}
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}

export default App;
