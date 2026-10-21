from pydantic import BaseModel,Field,Optional

class CourseCreate(BaseModel):
    title:str = Field(min_length=3,max_length=200)
    description:str | None = None
