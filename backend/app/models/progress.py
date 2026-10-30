from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Progress(Base):
    __tablename__ = "progress"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "lesson_id",
            name="uq_student_lesson_progress",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    completed_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    student = relationship("User", back_populates="progress_records")
    lesson = relationship("Lesson", back_populates="progress_records")