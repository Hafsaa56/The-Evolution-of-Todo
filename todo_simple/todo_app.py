"""
Simple in-memory todo console application.
Follows the specification: Python only, no external libraries, menu-based interaction.
"""

import sys
from typing import Dict, Optional


class Todo:
    """Simple todo item with id, title, description, and completion status."""

    def __init__(self, id: int, title: str, description: str = "", completed: bool = False):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed

    def __str__(self):
        status = "✓" if self.completed else "○"
        result = f"[{status}] {self.id}. {self.title}"
        if self.description:
            result += f"\n    Description: {self.description}"
        return result


class TodoApp:
    """Simple todo application with in-memory storage."""

    def __init__(self):
        self.todos: Dict[int, Todo] = {}
        self.next_id = 1

    def add_todo(self, title: str, description: str = "") -> Todo:
        """Add a new todo item."""
        if not title.strip():
            raise ValueError("Title is required")

        todo = Todo(id=self.next_id, title=title.strip(), description=description.strip())
        self.todos[self.next_id] = todo
        self.next_id += 1
        return todo

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """Get a todo by ID."""
        return self.todos.get(todo_id)

    def list_todos(self) -> list:
        """Get all todos."""
        return list(self.todos.values())

    def update_todo(self, todo_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> bool:
        """Update an existing todo."""
        if todo_id not in self.todos:
            return False

        todo = self.todos[todo_id]
        if title is not None:
            if title.strip():
                todo.title = title.strip()
            else:
                raise ValueError("Title cannot be empty")

        if description is not None:
            todo.description = description.strip()

        return True

    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo by ID."""
        if todo_id in self.todos:
            del self.todos[todo_id]
            return True
        return False

    def toggle_completion(self, todo_id: int) -> bool:
        """Toggle the completion status of a todo."""
        if todo_id not in self.todos:
            return False

        todo = self.todos[todo_id]
        todo.completed = not todo.completed
        return True


class TodoConsoleInterface:
    """Console interface for the todo application."""

    def __init__(self):
        self.app = TodoApp()

    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("TODO APPLICATION - MAIN MENU")
        print("="*50)
        print("1. Add a new task")
        print("2. View all tasks")
        print("3. Update an existing task")
        print("4. Delete a task")
        print("5. Mark a task as complete/incomplete")
        print("6. Exit")
        print("="*50)

    def get_user_choice(self) -> str:
        """Get user's menu choice."""
        try:
            choice = input("Enter your choice (1-6): ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye!")
            sys.exit(0)

    def add_task(self):
        """Add a new task."""
        print("\n--- ADD NEW TASK ---")
        try:
            title = input("Enter task title: ").strip()
            if not title:
                print("❌ Error: Title is required!")
                return

            description = input("Enter task description (optional, press Enter to skip): ").strip()

            todo = self.app.add_todo(title, description)
            print(f"✅ Task added successfully! ID: {todo.id}")
        except ValueError as e:
            print(f"❌ Error: {e}")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")

    def view_tasks(self):
        """View all tasks."""
        print("\n--- ALL TASKS ---")
        todos = self.app.list_todos()

        if not todos:
            print("No tasks found.")
            return

        for todo in todos:
            print(todo)
            print("-" * 40)

    def update_task(self):
        """Update an existing task."""
        print("\n--- UPDATE TASK ---")
        try:
            if not self.app.list_todos():
                print("No tasks available to update.")
                return

            task_id = int(input("Enter task ID to update: "))

            if not self.app.get_todo(task_id):
                print(f"❌ Error: Task with ID {task_id} not found!")
                return

            todo = self.app.get_todo(task_id)
            print(f"Current task: {todo}")

            new_title = input(f"Enter new title (current: '{todo.title}', press Enter to keep current): ").strip()
            new_title = new_title if new_title else None

            new_description = input(f"Enter new description (current: '{todo.description}', press Enter to keep current): ").strip()
            new_description = new_description if new_description else None

            if new_title is None and new_description is None:
                print("No changes made.")
                return

            if self.app.update_todo(task_id, new_title, new_description):
                print("✅ Task updated successfully!")
            else:
                print("❌ Error updating task!")

        except ValueError:
            print("❌ Error: Please enter a valid task ID (number)!")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")

    def delete_task(self):
        """Delete a task."""
        print("\n--- DELETE TASK ---")
        try:
            if not self.app.list_todos():
                print("No tasks available to delete.")
                return

            task_id = int(input("Enter task ID to delete: "))

            if self.app.delete_todo(task_id):
                print("✅ Task deleted successfully!")
            else:
                print(f"❌ Error: Task with ID {task_id} not found!")

        except ValueError:
            print("❌ Error: Please enter a valid task ID (number)!")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")

    def toggle_task_completion(self):
        """Toggle task completion status."""
        print("\n--- TOGGLE TASK COMPLETION ---")
        try:
            if not self.app.list_todos():
                print("No tasks available to toggle.")
                return

            task_id = int(input("Enter task ID to toggle: "))

            if self.app.toggle_completion(task_id):
                todo = self.app.get_todo(task_id)
                status = "completed" if todo.completed else "incomplete"
                print(f"✅ Task marked as {status}!")
            else:
                print(f"❌ Error: Task with ID {task_id} not found!")

        except ValueError:
            print("❌ Error: Please enter a valid task ID (number)!")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")

    def run(self):
        """Run the main application loop."""
        print("Welcome to the Todo Application!")
        print("All data exists only in memory and will be lost when program exits.")

        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.toggle_task_completion()
            elif choice == "6":
                print("\nThank you for using the Todo Application!")
                print("Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please enter a number between 1-6.")

            # Pause to let user see the result
            if choice in ["1", "2", "3", "4", "5"]:
                input("\nPress Enter to continue...")


def main():
    """Main entry point."""
    interface = TodoConsoleInterface()
    interface.run()


if __name__ == "__main__":
    main()