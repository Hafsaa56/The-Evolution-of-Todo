"""Todo domain models and interfaces."""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class TodoStatus(str, Enum):
    """Status of a todo item."""
    ACTIVE = "active"
    COMPLETED = "completed"


class Todo(BaseModel):
    """Todo entity model."""
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(min_length=1)
    description: Optional[str] = None
    status: TodoStatus = TodoStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def complete(self) -> None:
        """Mark the todo as completed."""
        self.status = TodoStatus.COMPLETED
        self.updated_at = datetime.now()

    def activate(self) -> None:
        """Mark the todo as active."""
        self.status = TodoStatus.ACTIVE
        self.updated_at = datetime.now()

    def update(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """Update the todo with new values."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()


class CreateTodoRequest(BaseModel):
    """Request model for creating a new todo."""
    title: str = Field(min_length=1)
    description: Optional[str] = None


class UpdateTodoRequest(BaseModel):
    """Request model for updating an existing todo."""
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = None
    status: Optional[TodoStatus] = None


class TodoResponse(BaseModel):
    """Response model for todo operations."""
    id: UUID
    title: str
    description: Optional[str]
    status: TodoStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_todo(cls, todo: Todo) -> 'TodoResponse':
        """Create a TodoResponse from a Todo entity."""
        return cls(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            status=todo.status,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )


class TodoFilter(BaseModel):
    """Filter model for querying todos."""
    status: Optional[TodoStatus] = None