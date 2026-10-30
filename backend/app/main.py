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
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentRead
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate, LessonRead
from app.models.progress import Progress
from app.schemas.progress import ProgressRead
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


@app.post("/courses/{course_id}/enroll", response_model=EnrollmentRead, status_code=201)
def enroll_in_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "student":
        raise HTTPException(
            status_code=403,
            detail="Only students can enroll in courses",
        )

    course = db.query(Course).filter(Course.id == course_id).first()

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    existing_enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == current_user.id,
            Enrollment.course_id == course_id,
        )
        .first()
    )

    if existing_enrollment:
        raise HTTPException(
            status_code=409,
            detail="You are already enrolled in this course",
        )

    enrollment = Enrollment(
        student_id=current_user.id,
        course_id=course_id,
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment


@app.get("/my-enrollments", response_model=list[EnrollmentRead])
def get_my_enrollments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "student":
        raise HTTPException(
            status_code=403,
            detail="Only students can view their enrollments",
        )

    enrollments = (
        db.query(Enrollment)
        .filter(Enrollment.student_id == current_user.id)
        .all()
    )

    return enrollments

@app.post("/courses/{course_id}/lessons", response_model=LessonRead, status_code=201)
def create_lesson(
    course_id: int,
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "instructor":
        raise HTTPException(status_code=403, detail="Only instructors can create lessons")

    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if course.instructor_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only add lessons to your own courses")

    lesson = Lesson(
        title=lesson_data.title,
        content=lesson_data.content,
        course_id=course.id,
    )

    db.add(lesson)
    db.commit()
    db.refresh(lesson)

    return lesson

@app.get("/courses/{course_id}/lessons", response_model=list[LessonRead])
def get_course_lessons(
    course_id: int,
    db: Session = Depends(get_db),
):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return db.query(Lesson).filter(Lesson.course_id == course_id).all()


@app.get("/courses/{course_id}/lessons/{lesson_id}", response_model=LessonRead)
def get_lesson(
    course_id: int,
    lesson_id: int,
    db: Session = Depends(get_db),
):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    lesson = (
        db.query(Lesson)
        .filter(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id,
        )
        .first()
    )

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return lesson

@app.put("/courses/{course_id}/lessons/{lesson_id}", response_model=LessonRead)
def update_lesson(
    course_id: int,
    lesson_id: int,
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "instructor":
        raise HTTPException(status_code=403, detail="Only instructors can update lessons")

    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if course.instructor_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update lessons in your own courses")

    lesson = (
        db.query(Lesson)
        .filter(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id,
        )
        .first()
    )

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    lesson.title = lesson_data.title
    lesson.content = lesson_data.content

    db.commit()
    db.refresh(lesson)

    return lesson


@app.delete("/courses/{course_id}/lessons/{lesson_id}", status_code=204)
def delete_lesson(
    course_id: int,
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "instructor":
        raise HTTPException(status_code=403, detail="Only instructors can delete lessons")

    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if course.instructor_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete lessons in your own courses")

    lesson = (
        db.query(Lesson)
        .filter(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id,
        )
        .first()
    )

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    db.delete(lesson)
    db.commit()

@app.post("/lessons/{lesson_id}/complete", response_model=ProgressRead, status_code=201)
def complete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Only students can complete lessons
    if current_user.role != "student":
        raise HTTPException(
            status_code=403,
            detail="Only students can complete lessons",
        )

    # Check whether the lesson exists
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # Check whether the student is enrolled in this lesson's course
    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == current_user.id,
            Enrollment.course_id == lesson.course_id,
        )
        .first()
    )

    if enrollment is None:
        raise HTTPException(
            status_code=403,
            detail="Enroll in the course before completing lessons",
        )

    # Prevent duplicate progress records
    existing_progress = (
        db.query(Progress)
        .filter(
            Progress.student_id == current_user.id,
            Progress.lesson_id == lesson_id,
        )
        .first()
    )

    if existing_progress is not None:
        raise HTTPException(
            status_code=409,
            detail="Lesson already completed",
        )

    # Save progress
    progress = Progress(
        student_id=current_user.id,
        lesson_id=lesson_id,
    )

    db.add(progress)
    db.commit()
    db.refresh(progress)

    return progress


@app.get("/my-progress", response_model=list[ProgressRead])
def get_my_progress(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "student":
        raise HTTPException(
            status_code=403,
            detail="Only students can view their progress",
        )

    progress_records = (
        db.query(Progress)
        .filter(Progress.student_id == current_user.id)
        .all()
    )

    return progress_records