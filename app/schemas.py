from uuid import UUID
from pydantic import BaseModel, field_validator
from datetime import datetime


class ItemIn(BaseModel):
    title: str
    description: str
    done: bool

    @field_validator("title")
    def validate_title(cls, value):
        if len(value) < 3:
            raise ValueError("Title must be at least 3 characters long")
        return value


class ItemOut(ItemIn):
    id: UUID
    created_at: datetime
    updated_at: datetime
