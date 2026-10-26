from fastapi import FastAPI
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate,UserLogin
from app.security import hash_password, verify_password, create_access_token
import jwt

from app.config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.models.course import Course
from app.schemas.course import CourseCreate,CourseRead

app = FastAPI(title="SkillTrack LMS")


@app.get("/")
def home():
    return {"message": "Welcome to SkillTrack LMS!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )
    hashed_password = hash_password(user_data.password)
    new_user = User(name=user_data.name,email=user_data.email,password_hash=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
    "message": "User registered successfully",
    "user_id": new_user.id,
    "name": new_user.name,
    "email": new_user.email
}

@app.post("/login")
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if not existing_user or not verify_password(
        user_data.password,
        existing_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(existing_user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET_KEY,
            algorithms=["HS256"]
        )

        user_id = int(payload["sub"])

    except (jwt.InvalidTokenError, KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    current_user = db.query(User).filter(User.id == user_id).first()

    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return current_user


@app.get("/me")
def get_my_profile(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }


@app.post("/courses")
def create_course(
    course_info: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "instructor":
        raise HTTPException(
            status_code=403,
            detail="Only instructors can create courses"
        )

    new_course = Course(
        title=course_info.title,
        description=course_info.description,
        instructor_id=current_user.id
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return {
        "id": new_course.id,
        "title": new_course.title,
        "description": new_course.description,
        "instructor_id": new_course.instructor_id
    }

@app.get("/courses", response_model=list[CourseRead])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses


@app.get("/courses/{course_id}", response_model=CourseRead)
def get_single_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course

@app.put("/courses/{course_id}", response_model=CourseRead)
def update_course(
    course_id: int,
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(Course.id == course_id).first()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    if course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own courses"
        )

    course.title = course_data.title
    course.description = course_data.description

    db.commit()
    db.refresh(course)

    return course

@app.delete("/courses/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(Course.id == course_id).first()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    if course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own courses"
        )

    db.delete(course)
    db.commit()

    return {"message": "Course deleted successfully"}