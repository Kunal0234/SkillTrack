from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.security import hash_password
from app.models.course import Course
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to SkillTrack LMS!"
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_student_cannot_create_course():
    response = client.post(
        "/register",
        json={
            "name": "Test Student",
            "email": "student_test@example.com",
            "password": "studentpass123"
        }
    )

    assert response.status_code == 200

    login_response = client.post(
        "/login",
        json={
            "email": "student_test@example.com",
            "password": "studentpass123"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    course_response = client.post(
        "/courses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Python Basics",
            "description": "Learn Python fundamentals"
        }
    )

    assert course_response.status_code == 403
    assert course_response.json()["detail"] == "Only instructors can create courses"


def test_instructor_can_create_course():
    db = TestingSessionLocal()

    instructor = User(
        name="Test Instructor",
        email="instructor_test@example.com",
        password_hash=hash_password("test_password"),
        role="instructor"
    )

    db.add(instructor)
    db.commit()
    db.refresh(instructor)

    instructor_id = instructor.id
    db.close()

    token_response = client.post(
        "/login",
        json={
            "email": "instructor_test@example.com",
            "password": "test_password"
        }
    )

    assert token_response.status_code == 200
    token = token_response.json()["access_token"]

    course_response = client.post(
        "/courses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Python Basics",
            "description": "Learn Python fundamentals"
        }
    )

    assert course_response.status_code == 200
    data = course_response.json()

    assert data["title"] == "Python Basics"
    assert data["description"] == "Learn Python fundamentals"
    assert data["instructor_id"] == instructor_id


def test_get_courses():
    response = client.get("/courses")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_instructor_can_update_own_course():
    db = TestingSessionLocal()

    instructor = User(
        name="Update Instructor",
        email="update_instructor@example.com",
        password_hash=hash_password("test_password"),
        role="instructor"
    )

    db.add(instructor)
    db.commit()
    db.refresh(instructor)
    instructor_id = instructor.id
    db.close()

    login_response = client.post(
        "/login",
        json={
            "email": "update_instructor@example.com",
            "password": "test_password"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/courses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Python Basics",
            "description": "Learn Python"
        }
    )

    assert create_response.status_code == 200
    course_id = create_response.json()["id"]

    update_response = client.put(
        f"/courses/{course_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Advanced Python",
            "description": "Learn advanced Python"
        }
    )

    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Advanced Python"
    assert update_response.json()["description"] == "Learn advanced Python"
    assert update_response.json()["instructor_id"] == instructor_id

def test_instructor_can_delete_own_course():
    db = TestingSessionLocal()

    instructor = User(
        name="Delete Instructor",
        email="delete_instructor@example.com",
        password_hash=hash_password("test_password"),
        role="instructor"
    )

    db.add(instructor)
    db.commit()
    db.refresh(instructor)
    db.close()

    login_response = client.post(
        "/login",
        json={
            "email": "delete_instructor@example.com",
            "password": "test_password"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/courses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Temporary Course",
            "description": "Course for delete testing"
        }
    )

    assert create_response.status_code == 200
    course_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/courses/{course_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Course deleted successfully"

    get_response = client.get(f"/courses/{course_id}")
    assert get_response.status_code == 404


def create_student_and_course(label):
    db = TestingSessionLocal()

    student = User(
        name="Enrollment Student",
        email=f"student_{label}@example.com",
        password_hash=hash_password("test_password"),
        role="student",
    )

    instructor = User(
        name="Enrollment Instructor",
        email=f"instructor_{label}@example.com",
        password_hash=hash_password("test_password"),
        role="instructor",
    )

    db.add_all([student, instructor])
    db.commit()
    db.refresh(instructor)

    course = Course(
        title="Enrollment Test Course",
        description="Course for enrollment testing",
        instructor_id=instructor.id,
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    course_id = course.id
    db.close()

    login_response = client.post(
        "/login",
        json={
            "email": f"student_{label}@example.com",
            "password": "test_password",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    return token, course_id


def test_student_can_enroll_in_course():
    token, course_id = create_student_and_course("success")

    response = client.post(
        f"/courses/{course_id}/enroll",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["course_id"] == course_id
    assert "student_id" in data
    assert "enrolled_at" in data


def test_student_cannot_enroll_twice():
    token, course_id = create_student_and_course("duplicate")

    headers = {"Authorization": f"Bearer {token}"}
    url = f"/courses/{course_id}/enroll"

    first_response = client.post(url, headers=headers)
    assert first_response.status_code == 201

    second_response = client.post(url, headers=headers)

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == (
        "You are already enrolled in this course"
    )


def test_student_cannot_enroll_in_nonexistent_course():
    token, _ = create_student_and_course("missing")

    response = client.post(
        "/courses/999999/enroll",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found"

def test_student_can_view_own_enrollments():
    token, course_id = create_student_and_course("view")

    headers = {"Authorization": f"Bearer {token}"}

    enroll_response = client.post(
        f"/courses/{course_id}/enroll",
        headers=headers,
    )
    assert enroll_response.status_code == 201

    response = client.get("/my-enrollments", headers=headers)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["course_id"] == course_id


def test_instructor_cannot_enroll_in_course():
    db = TestingSessionLocal()

    instructor = User(
        name="Restricted Instructor",
        email="restricted_instructor@example.com",
        password_hash=hash_password("test_password"),
        role="instructor",
    )

    db.add(instructor)
    db.commit()
    db.close()

    login_response = client.post(
        "/login",
        json={
            "email": "restricted_instructor@example.com",
            "password": "test_password",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.post(
        "/courses/999999/enroll",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Only students can enroll in courses"

def create_instructor_and_course(label):
    db = TestingSessionLocal()

    instructor = User(
        name="Lesson Instructor",
        email=f"lesson_instructor_{label}@example.com",
        password_hash=hash_password("test_password"),
        role="instructor",
    )

    db.add(instructor)
    db.commit()
    db.refresh(instructor)

    course = Course(
        title="Lesson Test Course",
        description="Course for lesson testing",
        instructor_id=instructor.id,
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    course_id = course.id
    db.close()

    login_response = client.post(
        "/login",
        json={
            "email": f"lesson_instructor_{label}@example.com",
            "password": "test_password",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    return token, course_id

def test_instructor_can_create_lesson():
    token, course_id = create_instructor_and_course("create")

    response = client.post(
        f"/courses/{course_id}/lessons",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Introduction to Python",
            "content": "Learn Python fundamentals",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Introduction to Python"
    assert data["content"] == "Learn Python fundamentals"
    assert data["course_id"] == course_id
    assert "id" in data

def test_student_cannot_create_lesson():
    student_token, course_id = create_student_and_course("lesson_restricted")

    response = client.post(
        f"/courses/{course_id}/lessons",
        headers={"Authorization": f"Bearer {student_token}"},
        json={
            "title": "Unauthorized Lesson",
            "content": "A student should not create this",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Only instructors can create lessons"

def test_instructor_cannot_create_lesson_in_another_instructors_course():
    _, course_id = create_instructor_and_course("owner")

    other_token, _ = create_instructor_and_course("other")

    response = client.post(
        f"/courses/{course_id}/lessons",
        headers={"Authorization": f"Bearer {other_token}"},
        json={
            "title": "Unauthorized Lesson",
            "content": "This instructor does not own the course",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You can only add lessons to your own courses"
    )

def test_instructor_can_list_course_lessons():
    token, course_id = create_instructor_and_course("list")

    create_response = client.post(
        f"/courses/{course_id}/lessons",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Python Introduction",
            "content": "Python basics",
        },
    )
    assert create_response.status_code == 201

    response = client.get(f"/courses/{course_id}/lessons")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Python Introduction"
    assert data[0]["course_id"] == course_id

def test_get_single_lesson():
    token, course_id = create_instructor_and_course("get_one")

    create_response = client.post(
        f"/courses/{course_id}/lessons",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "FastAPI Introduction",
            "content": "Learn FastAPI basics",
        },
    )
    assert create_response.status_code == 201

    lesson_id = create_response.json()["id"]

    response = client.get(
        f"/courses/{course_id}/lessons/{lesson_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == lesson_id
    assert response.json()["title"] == "FastAPI Introduction"

def test_instructor_can_update_lesson():
    token, course_id = create_instructor_and_course("update")

    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        f"/courses/{course_id}/lessons",
        headers=headers,
        json={
            "title": "Python Basics",
            "content": "Basic concepts",
        },
    )
    assert create_response.status_code == 201

    lesson_id = create_response.json()["id"]

    response = client.put(
        f"/courses/{course_id}/lessons/{lesson_id}",
        headers=headers,
        json={
            "title": "Advanced Python",
            "content": "Advanced concepts",
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Advanced Python"
    assert response.json()["content"] == "Advanced concepts"

def test_instructor_can_delete_lesson():
    token, course_id = create_instructor_and_course("delete")

    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        f"/courses/{course_id}/lessons",
        headers=headers,
        json={
            "title": "Temporary Lesson",
            "content": "This lesson will be deleted",
        },
    )
    assert create_response.status_code == 201

    lesson_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/courses/{course_id}/lessons/{lesson_id}",
        headers=headers,
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/courses/{course_id}/lessons/{lesson_id}"
    )
    assert get_response.status_code == 404

def test_instructor_cannot_update_another_instructors_lesson():
    owner_token, course_id = create_instructor_and_course("update_owner")
    other_token, _ = create_instructor_and_course("update_other")

    create_response = client.post(
        f"/courses/{course_id}/lessons",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={
            "title": "Original Lesson",
            "content": "Original content",
        },
    )
    assert create_response.status_code == 201

    lesson_id = create_response.json()["id"]

    response = client.put(
        f"/courses/{course_id}/lessons/{lesson_id}",
        headers={"Authorization": f"Bearer {other_token}"},
        json={
            "title": "Modified Lesson",
            "content": "Modified content",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You can only update lessons in your own courses"
    )


def test_instructor_cannot_delete_another_instructors_lesson():
    owner_token, course_id = create_instructor_and_course("delete_owner")
    other_token, _ = create_instructor_and_course("delete_other")

    create_response = client.post(
        f"/courses/{course_id}/lessons",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={
            "title": "Protected Lesson",
            "content": "This lesson belongs to another instructor",
        },
    )
    assert create_response.status_code == 201

    lesson_id = create_response.json()["id"]

    response = client.delete(
        f"/courses/{course_id}/lessons/{lesson_id}",
        headers={"Authorization": f"Bearer {other_token}"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You can only delete lessons in your own courses"
    )

def test_cannot_list_lessons_for_nonexistent_course():
    response = client.get("/courses/999999/lessons")

    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found"


def test_cannot_get_nonexistent_lesson():
    token, course_id = create_instructor_and_course("missing_lesson")

    response = client.get(
        f"/courses/{course_id}/lessons/999999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Lesson not found"