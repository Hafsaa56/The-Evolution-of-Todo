"""Tests for the todo use cases."""

import pytest
from uuid import UUID

from todo_app.application.use_cases import (
    AddTodoUseCase,
    CompleteTodoUseCase,
    DeleteTodoUseCase,
    EditTodoUseCase,
    FilterTodosUseCase,
    ListTodosUseCase
)
from todo_app.domain.models import (
    CreateTodoRequest,
    TodoFilter,
    TodoStatus,
    UpdateTodoRequest
)
from todo_app.infrastructure.repositories import InMemoryTodoRepository


class TestAddTodoUseCase:
    """Tests for the AddTodoUseCase."""

    @pytest.fixture
    def repository(self):
        """Create a fresh repository for each test."""
        return InMemoryTodoRepository()

    @pytest.fixture
    def use_case(self, repository):
        """Create the use case with a repository."""
        return AddTodoUseCase(repository)

    @pytest.mark.asyncio
    async def test_add_todo_success(self, use_case, repository):
        """Test successfully adding a todo."""
        request = CreateTodoRequest(title="Test todo", description="Test description")

        result = await use_case.execute(request)

        assert result.title == "Test todo"
        assert result.description == "Test description"
        assert result.status == TodoStatus.ACTIVE
        assert len(repository._todos) == 1

    @pytest.mark.asyncio
    async def test_add_todo_without_description(self, use_case, repository):
        """Test adding a todo without description."""
        request = CreateTodoRequest(title="Test todo")

        result = await use_case.execute(request)

        assert result.title == "Test todo"
        assert result.description is None
        assert len(repository._todos) == 1


class TestListTodosUseCase:
    """Tests for the ListTodosUseCase."""

    @pytest.fixture
    def repository(self):
        """Create a fresh repository for each test."""
        return InMemoryTodoRepository()

    @pytest.fixture
    def use_case(self, repository):
        """Create the use case with a repository."""
        return ListTodosUseCase(repository)

    @pytest.mark.asyncio
    async def test_list_all_todos(self, use_case, repository):
        """Test listing all todos."""
        # Add some todos
        add_use_case = AddTodoUseCase(repository)
        await add_use_case.execute(CreateTodoRequest(title="Todo 1"))
        await add_use_case.execute(CreateTodoRequest(title="Todo 2"))

        result = await use_case.execute()

        assert len(result) == 2
        titles = {todo.title for todo in result}
        assert titles == {"Todo 1", "Todo 2"}

    @pytest.mark.asyncio
    async def test_list_empty(self, use_case):
        """Test listing when no todos exist."""
        result = await use_case.execute()

        assert len(result) == 0


class TestCompleteTodoUseCase:
    """Tests for the CompleteTodoUseCase."""

    @pytest.fixture
    def repository(self):
        """Create a fresh repository for each test."""
        return InMemoryTodoRepository()

    @pytest.fixture
    def use_case(self, repository):
        """Create the use case with a repository."""
        return CompleteTodoUseCase(repository)

    @pytest.mark.asyncio
    async def test_complete_todo_success(self, use_case, repository):
        """Test successfully completing a todo."""
        # Add a todo first
        add_use_case = AddTodoUseCase(repository)
        created_todo = await add_use_case.execute(CreateTodoRequest(title="Test todo"))

        result = await use_case.execute(created_todo.id)

        assert result.id == created_todo.id
        assert result.status == TodoStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_complete_todo_not_found(self, use_case):
        """Test completing a todo that doesn't exist."""
        fake_id = UUID(int=12345)

        with pytest.raises(ValueError, match=f"Todo with ID {fake_id} not found"):
            await use_case.execute(fake_id)


class TestDeleteTodoUseCase:
    """Tests for the DeleteTodoUseCase."""

    @pytest.fixture
    def repository(self):
        """Create a fresh repository for each test."""
        return InMemoryTodoRepository()

    @pytest.fixture
    def use_case(self, repository):
        """Create the use case with a repository."""
        return DeleteTodoUseCase(repository)

    @pytest.mark.asyncio
    async def test_delete_todo_success(self, use_case, repository):
        """Test successfully deleting a todo."""
        # Add a todo first
        add_use_case = AddTodoUseCase(repository)
        created_todo = await add_use_case.execute(CreateTodoRequest(title="Test todo"))

        result = await use_case.execute(created_todo.id)

        assert result is True
        assert len(repository._todos) == 0

    @pytest.mark.asyncio
    async def test_delete_todo_not_found(self, use_case):
        """Test deleting a todo that doesn't exist."""
        fake_id = UUID(int=12345)

        with pytest.raises(ValueError, match=f"Todo with ID {fake_id} not found"):
            await use_case.execute(fake_id)


class TestEditTodoUseCase:
    """Tests for the EditTodoUseCase."""

    @pytest.fixture
    def repository(self):
        """Create a fresh repository for each test."""
        return InMemoryTodoRepository()

    @pytest.fixture
    def use_case(self, repository):
        """Create the use case with a repository."""
        return EditTodoUseCase(repository)

    @pytest.mark.asyncio
    async def test_edit_todo_success(self, use_case, repository):
        """Test successfully editing a todo."""
        # Add a todo first
        add_use_case = AddTodoUseCase(repository)
        created_todo = await add_use_case.execute(CreateTodoRequest(title="Original title"))

        update_request = UpdateTodoRequest(title="Updated title", description="Updated description")
        result = await use_case.execute((created_todo.id, update_request))

        assert result.id == created_todo.id
        assert result.title == "Updated title"
        assert result.description == "Updated description"

    @pytest.mark.asyncio
    async def test_edit_todo_not_found(self, use_case):
        """Test editing a todo that doesn't exist."""
        fake_id = UUID(int=12345)
        update_request = UpdateTodoRequest(title="Updated title")

        with pytest.raises(ValueError, match=f"Todo with ID {fake_id} not found"):
            await use_case.execute((fake_id, update_request))


class TestFilterTodosUseCase:
    """Tests for the FilterTodosUseCase."""

    @pytest.fixture
    def repository(self):
        """Create a fresh repository for each test."""
        return InMemoryTodoRepository()

    @pytest.fixture
    def use_case(self, repository):
        """Create the use case with a repository."""
        return FilterTodosUseCase(repository)

    @pytest.mark.asyncio
    async def test_filter_active_todos(self, use_case, repository):
        """Test filtering todos by active status."""
        # Add an active and a completed todo
        add_use_case = AddTodoUseCase(repository)
        active_todo = await add_use_case.execute(CreateTodoRequest(title="Active todo"))
        completed_todo = await add_use_case.execute(CreateTodoRequest(title="Completed todo"))

        # Complete the second todo
        complete_use_case = CompleteTodoUseCase(repository)
        await complete_use_case.execute(completed_todo.id)

        # Filter by active status
        active_filter = TodoFilter(status=TodoStatus.ACTIVE)
        result = await use_case.execute(active_filter)

        assert len(result) == 1
        assert result[0].id == active_todo.id
        assert result[0].status == TodoStatus.ACTIVE

    @pytest.mark.asyncio
    async def test_filter_completed_todos(self, use_case, repository):
        """Test filtering todos by completed status."""
        # Add an active and a completed todo
        add_use_case = AddTodoUseCase(repository)
        active_todo = await add_use_case.execute(CreateTodoRequest(title="Active todo"))
        completed_todo = await add_use_case.execute(CreateTodoRequest(title="Completed todo"))

        # Complete the second todo
        complete_use_case = CompleteTodoUseCase(repository)
        await complete_use_case.execute(completed_todo.id)

        # Filter by completed status
        completed_filter = TodoFilter(status=TodoStatus.COMPLETED)
        result = await use_case.execute(completed_filter)

        assert len(result) == 1
        assert result[0].id == completed_todo.id
        assert result[0].status == TodoStatus.COMPLETED