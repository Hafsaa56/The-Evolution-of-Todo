"""Todo application use cases."""

from typing import List, Optional
from uuid import UUID

from todo_app.application.base import UseCase
from todo_app.domain.models import (
    CreateTodoRequest,
    Todo,
    TodoFilter,
    TodoResponse,
    TodoStatus,
    UpdateTodoRequest
)
from todo_app.domain.repository import TodoRepository


class AddTodoUseCase(UseCase[CreateTodoRequest, TodoResponse]):
    """Use case for adding a new todo."""

    def __init__(self, repository: TodoRepository):
        self._repository = repository

    async def execute(self, input_data: CreateTodoRequest) -> TodoResponse:
        """Execute the add todo use case."""
        todo = Todo(
            title=input_data.title,
            description=input_data.description
        )
        saved_todo = await self._repository.create(todo)
        return TodoResponse.from_todo(saved_todo)


class ListTodosUseCase(UseCase[Optional[TodoFilter], List[TodoResponse]]):
    """Use case for listing todos."""

    def __init__(self, repository: TodoRepository):
        self._repository = repository

    async def execute(self, input_data: Optional[TodoFilter] = None) -> List[TodoResponse]:
        """Execute the list todos use case."""
        todos = await self._repository.list(input_data)
        return [TodoResponse.from_todo(todo) for todo in todos]


class CompleteTodoUseCase(UseCase[UUID, TodoResponse]):
    """Use case for completing a todo."""

    def __init__(self, repository: TodoRepository):
        self._repository = repository

    async def execute(self, input_data: UUID) -> TodoResponse:
        """Execute the complete todo use case."""
        todo = await self._repository.get_by_id(input_data)
        if not todo:
            raise ValueError(f"Todo with ID {input_data} not found")

        todo.complete()
        updated_todo = await self._repository.update(input_data, todo)
        if not updated_todo:
            raise ValueError(f"Failed to update todo with ID {input_data}")

        return TodoResponse.from_todo(updated_todo)


class DeleteTodoUseCase(UseCase[UUID, bool]):
    """Use case for deleting a todo."""

    def __init__(self, repository: TodoRepository):
        self._repository = repository

    async def execute(self, input_data: UUID) -> bool:
        """Execute the delete todo use case."""
        success = await self._repository.delete(input_data)
        if not success:
            raise ValueError(f"Todo with ID {input_data} not found")
        return success


class EditTodoUseCase(UseCase[tuple[UUID, UpdateTodoRequest], TodoResponse]):
    """Use case for editing a todo."""

    def __init__(self, repository: TodoRepository):
        self._repository = repository

    async def execute(self, input_data: tuple[UUID, UpdateTodoRequest]) -> TodoResponse:
        """Execute the edit todo use case."""
        todo_id, update_request = input_data
        todo = await self._repository.get_by_id(todo_id)
        if not todo:
            raise ValueError(f"Todo with ID {todo_id} not found")

        # Apply updates
        if update_request.title is not None:
            todo.title = update_request.title
        if update_request.description is not None:
            todo.description = update_request.description
        if update_request.status is not None:
            todo.status = update_request.status

        updated_todo = await self._repository.update(todo_id, todo)
        if not updated_todo:
            raise ValueError(f"Failed to update todo with ID {todo_id}")

        return TodoResponse.from_todo(updated_todo)


class FilterTodosUseCase(UseCase[TodoFilter, List[TodoResponse]]):
    """Use case for filtering todos by status."""

    def __init__(self, repository: TodoRepository):
        self._repository = repository

    async def execute(self, input_data: TodoFilter) -> List[TodoResponse]:
        """Execute the filter todos use case."""
        todos = await self._repository.list(input_data)
        return [TodoResponse.from_todo(todo) for todo in todos]