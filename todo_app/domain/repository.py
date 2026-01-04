"""Todo repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from todo_app.domain.models import Todo, TodoFilter


class TodoRepository(ABC):
    """Abstract base class for todo repository implementations."""

    @abstractmethod
    async def create(self, todo: Todo) -> Todo:
        """Create a new todo."""
        pass

    @abstractmethod
    async def get_by_id(self, todo_id: UUID) -> Optional[Todo]:
        """Get a todo by its ID."""
        pass

    @abstractmethod
    async def list(self, filters: Optional[TodoFilter] = None) -> List[Todo]:
        """List todos with optional filtering."""
        pass

    @abstractmethod
    async def update(self, todo_id: UUID, todo: Todo) -> Optional[Todo]:
        """Update an existing todo."""
        pass

    @abstractmethod
    async def delete(self, todo_id: UUID) -> bool:
        """Delete a todo by its ID."""
        pass