const API_BASE_URL = "http://127.0.0.1:8000";

export async function registerUser(userData) {
  const response = await fetch(`${API_BASE_URL}/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Registration failed");
  }

  return data;
}

export async function loginUser(userData) {
  const response = await fetch(`${API_BASE_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Login failed");
  }

  return data;
}

export async function getMyProfile(token) {
  const response = await fetch(`${API_BASE_URL}/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not fetch profile");
  }

  return data;
}

export async function getInstructorCourses(token) {
  const response = await fetch(`${API_BASE_URL}/instructor/courses`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not fetch instructor courses");
  }

  return data;
}

export async function getMyEnrollments(token) {
  const response = await fetch(`${API_BASE_URL}/my-enrollments`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not fetch enrollments");
  }

  return data;
}

export async function getMyProgress(token) {
  const response = await fetch(`${API_BASE_URL}/my-progress`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not fetch progress");
  }

  return data;
}

export async function getCourses() {
  const response = await fetch(`${API_BASE_URL}/courses`);

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not fetch courses");
  }

  return data;
}
export async function enrollInCourse(courseId, token) {
  const response = await fetch(`${API_BASE_URL}/courses/${courseId}/enroll`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Enrollment failed");
  }

  return data;
}
export async function createCourse(courseData, token) {
  const response = await fetch(`${API_BASE_URL}/courses`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(courseData),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Course creation failed");
  }

  return data;
}

export async function getInstructorApplications(token) {
  const response = await fetch(
    `${API_BASE_URL}/admin/instructor-applications`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not fetch applications");
  }

  return data;
}

export async function reviewInstructorApplication(
  applicationId,
  status,
  token
) {
  const response = await fetch(
    `${API_BASE_URL}/admin/instructor-applications/${applicationId}`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ status }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not review application");
  }

  return data;
}


export async function updateCourse(courseId, courseData, token) {
  const response = await fetch(`${API_BASE_URL}/courses/${courseId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(courseData),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Course update failed");
  }

  return data;
}

export async function deleteCourse(courseId, token) {
  const response = await fetch(`${API_BASE_URL}/courses/${courseId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Course deletion failed");
  }

  return data;
}
