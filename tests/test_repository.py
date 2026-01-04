"""Tests for the todo repository implementations."""

import pytest
from uuid import UUID

from todo_app.domain.models import Todo, TodoFilter, TodoStatus
from todo_app.infrastructure.repositories import InMemoryTodoRepository


class TestInMemoryTodoRepository:
    """Tests for the InMemoryTodoRepository."""

    @pytest.fixture
    def repository(self):
        """Create a fresh repository for each test."""
        return InMemoryTodoRepository()

    @pytest.mark.asyncio
    async def test_create_todo(self, repository):
        """Test creating a todo."""
        todo = Todo(title="Test todo")

        result = await repository.create(todo)

        assert result.id == todo.id
        assert result.title == "Test todo"
        assert len(repository._todos) == 1

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repository):
        """Test getting a todo by ID that exists."""
        original_todo = Todo(title="Test todo")
        await repository.create(original_todo)

        result = await repository.get_by_id(original_todo.id)

        assert result is not None
        assert result.id == original_todo.id
        assert result.title == "Test todo"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repository):
        """Test getting a todo by ID that doesn't exist."""
        result = await repository.get_by_id(UUID(int=12345))

        assert result is None

    @pytest.mark.asyncio
    async def test_list_all_todos(self, repository):
        """Test listing all todos."""
        todo1 = Todo(title="Todo 1")
        todo2 = Todo(title="Todo 2")
        await repository.create(todo1)
        await repository.create(todo2)

        result = await repository.list()

        assert len(result) == 2
        titles = {todo.title for todo in result}
        assert titles == {"Todo 1", "Todo 2"}

    @pytest.mark.asyncio
    async def test_list_filtered_todos_by_status(self, repository):
        """Test listing todos filtered by status."""
        active_todo = Todo(title="Active todo")
        completed_todo = Todo(title="Completed todo")
        completed_todo.complete()
        await repository.create(active_todo)
        await repository.create(completed_todo)

        # Filter by active status
        active_filter = TodoFilter(status=TodoStatus.ACTIVE)
        active_result = await repository.list(active_filter)
        assert len(active_result) == 1
        assert active_result[0].status == TodoStatus.ACTIVE

        # Filter by completed status
        completed_filter = TodoFilter(status=TodoStatus.COMPLETED)
        completed_result = await repository.list(completed_filter)
        assert len(completed_result) == 1
        assert completed_result[0].status == TodoStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_update_todo(self, repository):
        """Test updating a todo."""
        original_todo = Todo(title="Original title")
        await repository.create(original_todo)

        updated_todo = Todo(
            id=original_todo.id,
            title="Updated title",
            description="Updated description"
        )
        result = await repository.update(original_todo.id, updated_todo)

        assert result is not None
        assert result.title == "Updated title"
        assert result.description == "Updated description"

    @pytest.mark.asyncio
    async def test_update_todo_not_found(self, repository):
        """Test updating a todo that doesn't exist."""
        fake_id = UUID(int=12345)
        todo = Todo(id=fake_id, title="Test")

        result = await repository.update(fake_id, todo)

        assert result is None

    @pytest.mark.asyncio
    async def test_delete_todo(self, repository):
        """Test deleting a todo."""
        todo = Todo(title="Todo to delete")
        await repository.create(todo)

        result = await repository.delete(todo.id)

        assert result is True
        assert len(repository._todos) == 0

    @pytest.mark.asyncio
    async def test_delete_todo_not_found(self, repository):
        """Test deleting a todo that doesn't exist."""
        fake_id = UUID(int=12345)

        result = await repository.delete(fake_id)

        assert result is False