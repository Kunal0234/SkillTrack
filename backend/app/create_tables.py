from app.database import Base, engine
from app.models.user import User
from app.models.course import Course
from app.models.enrollment import Enrollment
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")