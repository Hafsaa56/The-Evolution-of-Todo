import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
import uuid

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        if len(v.strip()) < 1:
            raise ValueError('Title must be at least 1 character long')
        if len(v) > 200:
            raise ValueError('Title must be less than 200 characters')
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v is not None and len(v) > 2000:
            raise ValueError('Description must be less than 2000 characters')
        return v

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Title cannot be empty')
            if len(v.strip()) < 1:
                raise ValueError('Title must be at least 1 character long')
            if len(v) > 200:
                raise ValueError('Title must be less than 200 characters')
            return v.strip()
        return v

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v is not None and len(v) > 2000:
            raise ValueError('Description must be less than 2000 characters')
        return v

class TaskResponse(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True