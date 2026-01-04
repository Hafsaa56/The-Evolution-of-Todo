"""Main CLI entry point for the todo application."""

import argparse
import asyncio
import json
import sys
from typing import Any, Dict
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


class TodoCLI:
    """Command-line interface for the todo application."""

    def __init__(self):
        self.repository = InMemoryTodoRepository()
        self.add_todo = AddTodoUseCase(self.repository)
        self.list_todos = ListTodosUseCase(self.repository)
        self.complete_todo = CompleteTodoUseCase(self.repository)
        self.delete_todo = DeleteTodoUseCase(self.repository)
        self.edit_todo = EditTodoUseCase(self.repository)
        self.filter_todos = FilterTodosUseCase(self.repository)

    def _format_output(self, data: Any, json_format: bool = False) -> str:
        """Format output as either human-readable or JSON."""
        if json_format:
            if isinstance(data, list):
                return json.dumps([item.model_dump() for item in data], indent=2, default=str)
            else:
                return json.dumps(data.model_dump(), indent=2, default=str)
        else:
            # Human-readable format
            if isinstance(data, list):
                if not data:
                    return "No todos found."

                output_lines = []
                for item in data:
                    status_symbol = "✓" if item.status == TodoStatus.COMPLETED else "○"
                    output_lines.append(f"{status_symbol} [{item.id}] {item.title}")
                    if item.description:
                        output_lines.append(f"    {item.description}")
                    output_lines.append("")
                return "\n".join(output_lines).strip()
            else:
                if hasattr(data, 'title'):
                    status_symbol = "✓" if data.status == TodoStatus.COMPLETED else "○"
                    output = f"{status_symbol} [{data.id}] {data.title}"
                    if hasattr(data, 'description') and data.description:
                        output += f"\n    {data.description}"
                    return output
                return str(data)

    async def add(self, title: str, description: str = None, json_format: bool = False):
        """Add a new todo."""
        try:
            request = CreateTodoRequest(title=title, description=description)
            result = await self.add_todo.execute(request)
            print(self._format_output(result, json_format))
        except Exception as e:
            print(f"Error adding todo: {str(e)}", file=sys.stderr)
            sys.exit(1)

    async def list(self, json_format: bool = False, status: str = None):
        """List all todos."""
        try:
            filters = None
            if status:
                status_enum = TodoStatus(status.lower())
                filters = TodoFilter(status=status_enum)

            result = await self.list_todos.execute(filters)
            print(self._format_output(result, json_format))
        except Exception as e:
            print(f"Error listing todos: {str(e)}", file=sys.stderr)
            sys.exit(1)

    async def complete(self, todo_id: str, json_format: bool = False):
        """Complete a todo."""
        try:
            uuid_id = UUID(todo_id)
            result = await self.complete_todo.execute(uuid_id)
            print(self._format_output(result, json_format))
        except ValueError as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error completing todo: {str(e)}", file=sys.stderr)
            sys.exit(1)

    async def delete(self, todo_id: str, json_format: bool = False):
        """Delete a todo."""
        try:
            uuid_id = UUID(todo_id)
            result = await self.delete_todo.execute(uuid_id)
            if json_format:
                print(json.dumps({"success": result}))
            else:
                print(f"Todo {todo_id} deleted successfully." if result else f"Todo {todo_id} not found.")
        except ValueError as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error deleting todo: {str(e)}", file=sys.stderr)
            sys.exit(1)

    async def edit(self, todo_id: str, title: str = None, description: str = None, json_format: bool = False):
        """Edit a todo."""
        try:
            uuid_id = UUID(todo_id)
            request = UpdateTodoRequest(title=title, description=description)
            result = await self.edit_todo.execute((uuid_id, request))
            print(self._format_output(result, json_format))
        except ValueError as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error editing todo: {str(e)}", file=sys.stderr)
            sys.exit(1)

    def _validate_todo_id(self, value: str) -> str:
        """Validate that the provided value is a valid UUID."""
        try:
            UUID(value)
            return value
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid UUID: {value}")

    def run(self):
        """Run the CLI application."""
        parser = argparse.ArgumentParser(description="Todo CLI Application")
        parser.add_argument("--json", action="store_true", help="Output in JSON format")

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Add command
        add_parser = subparsers.add_parser("add", help="Add a new todo")
        add_parser.add_argument("--title", "-t", required=True, help="Todo title")
        add_parser.add_argument("--description", "-d", help="Todo description")

        # List command
        list_parser = subparsers.add_parser("list", help="List all todos")
        list_parser.add_argument(
            "--status",
            choices=["active", "completed"],
            help="Filter todos by status"
        )

        # Complete command
        complete_parser = subparsers.add_parser("complete", help="Complete a todo")
        complete_parser.add_argument("id", type=self._validate_todo_id, help="Todo ID to complete")

        # Delete command
        delete_parser = subparsers.add_parser("delete", help="Delete a todo")
        delete_parser.add_argument("id", type=self._validate_todo_id, help="Todo ID to delete")

        # Edit command
        edit_parser = subparsers.add_parser("edit", help="Edit a todo")
        edit_parser.add_argument("id", type=self._validate_todo_id, help="Todo ID to edit")
        edit_parser.add_argument("--title", "-t", help="New title")
        edit_parser.add_argument("--description", "-d", help="New description")

        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            sys.exit(1)

        # Run the appropriate command
        command_map = {
            "add": lambda: self.add(args.title, args.description, args.json),
            "list": lambda: self.list(args.json, args.status),
            "complete": lambda: self.complete(args.id, args.json),
            "delete": lambda: self.delete(args.id, args.json),
            "edit": lambda: self.edit(args.id, args.title, args.description, args.json),
        }

        try:
            asyncio.run(command_map[args.command]())
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.", file=sys.stderr)
            sys.exit(1)


def main():
    """Main entry point."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()