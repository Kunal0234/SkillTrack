from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class InstructorApplicationCreate(BaseModel):
    reason: str = Field(min_length=20, max_length=1000)


class InstructorApplicationRead(BaseModel):
    id: int
    user_id: int
    reason: str
    status: Literal["pending", "approved", "rejected"]
    reviewed_by: int | None
    created_at: datetime
    reviewed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class InstructorApplicationReview(BaseModel):
    status: Literal["approved", "rejected"]
