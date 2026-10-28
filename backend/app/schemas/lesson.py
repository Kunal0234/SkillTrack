from pydantic import BaseModel, Field, ConfigDict


class LessonCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str | None = None


class LessonRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str | None = None
    course_id: int