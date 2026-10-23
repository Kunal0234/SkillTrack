from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.security import hash_password

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
