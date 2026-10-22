from pydantic import BaseModel,Field,ConfigDict

class CourseCreate(BaseModel):
    title:str = Field(min_length=3,max_length=200)
    description:str | None = None

class CourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    title:str
    description:str | None = None
    instructor_id:int