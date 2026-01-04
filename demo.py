"""
Demo script showing how to use the todo application programmatically.
This demonstrates the functionality that would be available through the CLI.
"""

import asyncio
import uuid
from datetime import datetime

# Import the application components
from todo_app.application.use_cases import (
    AddTodoUseCase,
    CompleteTodoUseCase,
    DeleteTodoUseCase,
    EditTodoUseCase,
    ListTodosUseCase
)
from todo_app.domain.models import CreateTodoRequest, UpdateTodoRequest, TodoStatus
from todo_app.infrastructure.repositories import InMemoryTodoRepository


async def demo():
    """Demonstrate the todo application functionality."""
    print("=== Todo Application Demo ===\n")

    # Initialize the repository and use cases
    repository = InMemoryTodoRepository()

    add_todo = AddTodoUseCase(repository)
    list_todos = ListTodosUseCase(repository)
    complete_todo = CompleteTodoUseCase(repository)
    delete_todo = DeleteTodoUseCase(repository)
    edit_todo = EditTodoUseCase(repository)

    # 1. Add some todos
    print("1. Adding todos...")
    todo1 = await add_todo.execute(CreateTodoRequest(
        title="Buy groceries",
        description="Milk, bread, eggs, fruits"
    ))
    print(f"   Added: {todo1.title}")

    todo2 = await add_todo.execute(CreateTodoRequest(
        title="Finish project report",
        description="Complete the quarterly project report for review"
    ))
    print(f"   Added: {todo2.title}")

    todo3 = await add_todo.execute(CreateTodoRequest(
        title="Call dentist",
        description="Schedule appointment for next week"
    ))
    print(f"   Added: {todo3.title}\n")

    # 2. List all todos
    print("2. Listing all todos...")
    all_todos = await list_todos.execute()
    for todo in all_todos:
        status = "✓" if todo.status == TodoStatus.COMPLETED else "○"
        print(f"   {status} [{todo.id}] {todo.title}")
        if todo.description:
            print(f"      {todo.description}")
    print()

    # 3. Complete a todo
    print("3. Completing a todo...")
    completed = await complete_todo.execute(todo1.id)
    print(f"   Completed: {completed.title}\n")

    # 4. List active todos only
    print("4. Listing active todos...")
    from todo_app.domain.models import TodoFilter
    active_filter = TodoFilter(status=TodoStatus.ACTIVE)
    active_todos = await list_todos.execute(active_filter)
    for todo in active_todos:
        print(f"   ○ [{todo.id}] {todo.title}")
    print()

    # 5. Edit a todo
    print("5. Editing a todo...")
    updated = await edit_todo.execute((
        todo2.id,
        UpdateTodoRequest(title="Finish the important project report", description="Complete and submit by Friday")
    ))
    print(f"   Updated: {updated.title}\n")

    # 6. List all todos again to see changes
    print("6. Final list of all todos...")
    final_list = await list_todos.execute()
    for todo in final_list:
        status = "✓" if todo.status == TodoStatus.COMPLETED else "○"
        print(f"   {status} [{todo.id}] {todo.title}")
    print()

    # 7. Delete a todo
    print("7. Deleting a todo...")
    delete_success = await delete_todo.execute(todo3.id)
    print(f"   Deleted: {delete_success}\n")

    # 8. Final list
    print("8. Final list after deletion...")
    final_list = await list_todos.execute()
    for todo in final_list:
        status = "✓" if todo.status == TodoStatus.COMPLETED else "○"
        print(f"   {status} [{todo.id}] {todo.title}")
    print()


if __name__ == "__main__":
    asyncio.run(demo())