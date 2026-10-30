from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProgressRead(BaseModel):
    id: int
    student_id: int
    lesson_id: int
    completed_at: datetime

    model_config = ConfigDict(from_attributes=True)