"""Tests for the todo domain models."""

import pytest
from datetime import datetime
from uuid import UUID

from todo_app.domain.models import Todo, TodoStatus, CreateTodoRequest, UpdateTodoRequest


class TestTodo:
    """Tests for the Todo entity."""

    def test_create_todo(self):
        """Test creating a new todo."""
        todo = Todo(title="Test todo")

        assert todo.title == "Test todo"
        assert todo.status == TodoStatus.ACTIVE
        assert isinstance(todo.id, UUID)
        assert isinstance(todo.created_at, datetime)
        assert isinstance(todo.updated_at, datetime)

    def test_create_todo_with_description(self):
        """Test creating a todo with description."""
        todo = Todo(title="Test todo", description="Test description")

        assert todo.title == "Test todo"
        assert todo.description == "Test description"

    def test_complete_todo(self):
        """Test completing a todo."""
        todo = Todo(title="Test todo")

        todo.complete()

        assert todo.status == TodoStatus.COMPLETED
        assert todo.updated_at > todo.created_at

    def test_activate_todo(self):
        """Test activating a completed todo."""
        todo = Todo(title="Test todo")
        todo.complete()  # First complete it

        todo.activate()

        assert todo.status == TodoStatus.ACTIVE

    def test_update_todo(self):
        """Test updating a todo."""
        todo = Todo(title="Test todo", description="Original description")
        original_updated_at = todo.updated_at

        todo.update(title="Updated title", description="Updated description")

        assert todo.title == "Updated title"
        assert todo.description == "Updated description"
        assert todo.updated_at > original_updated_at

    def test_update_todo_partial(self):
        """Test updating only some fields of a todo."""
        todo = Todo(title="Test todo", description="Original description")
        original_title = todo.title

        todo.update(description="Updated description")

        assert todo.title == original_title  # Title should remain unchanged
        assert todo.description == "Updated description"


class TestCreateTodoRequest:
    """Tests for the CreateTodoRequest model."""

    def test_create_request_valid(self):
        """Test creating a valid request."""
        request = CreateTodoRequest(title="Test title")

        assert request.title == "Test title"
        assert request.description is None

    def test_create_request_with_description(self):
        """Test creating a request with description."""
        request = CreateTodoRequest(title="Test title", description="Test description")

        assert request.title == "Test title"
        assert request.description == "Test description"

    def test_create_request_empty_title(self):
        """Test creating a request with empty title should fail."""
        with pytest.raises(ValueError):
            CreateTodoRequest(title="")


class TestUpdateTodoRequest:
    """Tests for the UpdateTodoRequest model."""

    def test_update_request_partial(self):
        """Test creating an update request with partial data."""
        request = UpdateTodoRequest(title="New title")

        assert request.title == "New title"
        assert request.description is None
        assert request.status is None

    def test_update_request_full(self):
        """Test creating an update request with all fields."""
        request = UpdateTodoRequest(
            title="New title",
            description="New description",
            status=TodoStatus.COMPLETED
        )

        assert request.title == "New title"
        assert request.description == "New description"
        assert request.status == TodoStatus.COMPLETED