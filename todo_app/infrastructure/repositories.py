"""Todo repository implementations."""

import asyncio
from typing import Dict, List, Optional
from uuid import UUID

from todo_app.domain.models import Todo, TodoFilter, TodoStatus
from todo_app.domain.repository import TodoRepository


class InMemoryTodoRepository(TodoRepository):
    """In-memory implementation of the todo repository."""

    def __init__(self):
        self._todos: Dict[UUID, Todo] = {}
        self._lock = asyncio.Lock()

    async def create(self, todo: Todo) -> Todo:
        """Create a new todo."""
        async with self._lock:
            self._todos[todo.id] = todo
            return todo

    async def get_by_id(self, todo_id: UUID) -> Optional[Todo]:
        """Get a todo by its ID."""
        async with self._lock:
            return self._todos.get(todo_id)

    async def list(self, filters: Optional[TodoFilter] = None) -> List[Todo]:
        """List todos with optional filtering."""
        async with self._lock:
            todos = list(self._todos.values())

            if filters and filters.status:
                todos = [todo for todo in todos if todo.status == filters.status]

            return todos

    async def update(self, todo_id: UUID, todo: Todo) -> Optional[Todo]:
        """Update an existing todo."""
        async with self._lock:
            if todo_id not in self._todos:
                return None
            self._todos[todo_id] = todo
            return todo

    async def delete(self, todo_id: UUID) -> bool:
        """Delete a todo by its ID."""
        async with self._lock:
            if todo_id not in self._todos:
                return False
            del self._todos[todo_id]
            return True