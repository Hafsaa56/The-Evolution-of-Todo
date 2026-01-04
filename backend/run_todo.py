"""
Professional Todo Application - Main Entry Point
This is the only file you need to run for the best experience.
"""

import sys
from typing import Dict, Optional


class Colors:
    """ANSI color codes for professional terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Todo:
    """Professional todo item with clear status indicators."""

    def __init__(self, id: int, title: str, description: str = "", completed: bool = False):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = __import__('datetime').datetime.now()

    def get_status_symbol(self):
        """Get status symbol based on completion."""
        return "✓" if self.completed else "○"

    def get_status_text(self):
        """Get status text based on completion."""
        return "COMPLETED" if self.completed else "PENDING"

    def get_color(self):
        """Get appropriate color based on completion status."""
        return Colors.OKGREEN if self.completed else Colors.WARNING

    def __str__(self):
        status_symbol = self.get_status_symbol()
        status_text = self.get_status_text()
        color = self.get_color()

        result = f"{color}[{status_symbol}] ID: {self.id} - {self.title}{Colors.ENDC}"
        result += f"\n   Status: {color}{status_text}{Colors.ENDC}"
        if self.description:
            result += f"\n   Notes: {Colors.OKCYAN}{self.description}{Colors.ENDC}"
        result += f"\n   {'-' * 50}"
        return result


class TodoApp:
    """Professional todo application with clear statistics and management."""

    def __init__(self):
        self.todos: Dict[int, Todo] = {}
        self.next_id = 1

    def add_todo(self, title: str, description: str = "") -> Todo:
        """Add a new todo with validation."""
        if not title.strip():
            raise ValueError("Task title is required")

        todo = Todo(id=self.next_id, title=title.strip(), description=description.strip())
        self.todos[self.next_id] = todo
        self.next_id += 1
        return todo

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """Get a todo by ID."""
        return self.todos.get(todo_id)

    def list_todos(self, filter_completed: Optional[bool] = None) -> list:
        """Get todos with optional filtering."""
        todos = list(self.todos.values())

        if filter_completed is not None:
            todos = [todo for todo in todos if todo.completed == filter_completed]

        # Sort by status (pending first) and then by ID
        todos.sort(key=lambda x: (x.completed, x.id))
        return todos

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

    def get_statistics(self) -> dict:
        """Get comprehensive application statistics."""
        total = len(self.todos)
        completed = len([t for t in self.todos.values() if t.completed])
        pending = total - completed

        completion_percentage = (completed / total * 100) if total > 0 else 0

        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_percentage': completion_percentage
        }


class TodoConsoleInterface:
    """Professional console interface with clear user guidance."""

    def __init__(self):
        self.app = TodoApp()

    def clear_screen(self):
        """Clear screen for better user experience."""
        print("\033[H\033[J", end="")

    def display_header(self):
        """Display professional application header."""
        print(f"{Colors.HEADER}")
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 25 + "📋 PROFESSIONAL TODO APP 📋" + " " * 25 + "║")
        print("║" + " " * 20 + "Organize Your Tasks Efficiently" + " " * 21 + "║")
        print("╚" + "═" * 78 + "╝")
        print(f"{Colors.ENDC}")

    def display_statistics(self):
        """Display clear statistics with user-friendly metrics."""
        stats = self.app.get_statistics()

        print(f"\n{Colors.BOLD}📊 YOUR TASK SUMMARY{Colors.ENDC}")
        print("┌" + "─" * 30 + "┬" + "─" * 15 + "┬" + "─" * 15 + "┐")
        print(f"│ {Colors.OKBLUE}Total Tasks{Colors.ENDC}{' ' * 18} │ {Colors.OKGREEN}Completed{Colors.ENDC}{' ' * 5} │ {Colors.WARNING}Pending{Colors.ENDC}{' ' * 6} │")
        print("├" + "─" * 30 + "┼" + "─" * 15 + "┼" + "─" * 15 + "┤")
        print(f"│ {stats['total']:>28} │ {stats['completed']:>13} │ {stats['pending']:>13} │")
        print("└" + "─" * 30 + "┴" + "─" * 15 + "┴" + "─" * 15 + "┘")

        if stats['total'] > 0:
            print(f"\n{Colors.BOLD}🎯 COMPLETION PROGRESS:{Colors.ENDC}")
            completion_bar = "█" * int(stats['completion_percentage'] // 5)
            empty_bar = "░" * (20 - len(completion_bar))
            print(f"   [{Colors.OKGREEN}{completion_bar}{Colors.ENDC}{empty_bar}] {Colors.OKGREEN if stats['completion_percentage'] >= 50 else Colors.WARNING}{stats['completion_percentage']:.1f}%{Colors.ENDC}")

            # Motivational message
            if stats['completion_percentage'] >= 100:
                print(f"   🏆 {Colors.OKGREEN}EXCELLENT! You've completed all tasks!{Colors.ENDC}")
            elif stats['completion_percentage'] >= 75:
                print(f"   🌟 {Colors.OKGREEN}GREAT JOB! Keep up the good work!{Colors.ENDC}")
            elif stats['completion_percentage'] >= 50:
                print(f"   👍 {Colors.OKGREEN}GOOD PROGRESS! You're halfway there!{Colors.ENDC}")
            elif stats['completion_percentage'] > 0:
                print(f"   💪 {Colors.WARNING}KEEP GOING! You're making progress!{Colors.ENDC}")
            else:
                print(f"   🚀 {Colors.OKBLUE}TIME TO GET STARTED!{Colors.ENDC}")

    def display_menu(self):
        """Display professional menu with clear instructions."""
        print(f"\n{Colors.BOLD}📋 MAIN MENU - SELECT AN OPTION:{Colors.ENDC}")
        print("┌" + "─" * 78 + "┐")
        print(f"│ {Colors.OKBLUE}1. ➕ ADD NEW TASK{Colors.ENDC}{' ' * 58} │")
        print(f"│ {Colors.OKBLUE}2. 📋 VIEW ALL TASKS{Colors.ENDC}{' ' * 54} │")
        print(f"│ {Colors.OKBLUE}3. ✅ VIEW COMPLETED TASKS{Colors.ENDC}{' ' * 49} │")
        print(f"│ {Colors.OKBLUE}4. ⏳ VIEW PENDING TASKS{Colors.ENDC}{' ' * 51} │")
        print(f"│ {Colors.OKBLUE}5. ✏️  UPDATE EXISTING TASK{Colors.ENDC}{' ' * 48} │")
        print(f"│ {Colors.OKBLUE}6. 🗑️  DELETE TASK{Colors.ENDC}{' ' * 57} │")
        print(f"│ {Colors.OKBLUE}7. 🔄 MARK TASK COMPLETE/INCOMPLETE{Colors.ENDC}{' ' * 38} │")
        print(f"│ {Colors.OKBLUE}8. 📊 VIEW DETAILED STATISTICS{Colors.ENDC}{' ' * 44} │")
        print(f"│ {Colors.OKBLUE}9. 🚪 EXIT APPLICATION{Colors.ENDC}{' ' * 52} │")
        print("└" + "─" * 78 + "┘")
        print(f"\n{Colors.WARNING}💡 TIP: Enter the number of your choice (1-9){Colors.ENDC}")

    def get_user_choice(self) -> str:
        """Get user's menu choice with validation."""
        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-9): {Colors.ENDC}").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n{Colors.WARNING}👋 Goodbye! Thank you for using Professional Todo App.{Colors.ENDC}")
            sys.exit(0)

    def add_task(self):
        """Add a new task with clear instructions."""
        print(f"\n{Colors.HEADER}╔" + "═" * 78 + "╗{Colors.ENDC}")
        print(f"{Colors.HEADER}║{Colors.BOLD}                           ADD NEW TASK                              {Colors.ENDC}{Colors.HEADER}║{Colors.ENDC}")
        print(f"{Colors.HEADER}╚" + "═" * 78 + "╝{Colors.ENDC}")

        try:
            print(f"{Colors.BOLD}📝 Please enter the task details:{Colors.ENDC}")
            title = input("   Task Title (required): ").strip()
            if not title:
                print(f"   {Colors.FAIL}❌ ERROR: Task title is required!{Colors.ENDC}")
                return

            description = input("   Task Description (optional): ").strip()

            todo = self.app.add_todo(title, description)
            print(f"   {Colors.OKGREEN}✅ SUCCESS: Task added successfully!{Colors.ENDC}")
            print(f"   {Colors.OKCYAN}ID: {todo.id} | Title: {todo.title}{Colors.ENDC}")
            print(f"   {Colors.WARNING}💡 Remember: This task is stored in memory only{Colors.ENDC}")

        except ValueError as e:
            print(f"   {Colors.FAIL}❌ ERROR: {e}{Colors.ENDC}")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Colors.WARNING}   Operation cancelled.{Colors.ENDC}")

    def view_tasks(self, filter_completed: Optional[bool] = None):
        """View tasks with professional formatting."""
        print(f"\n{Colors.HEADER}╔" + "═" * 78 + "╗{Colors.ENDC}")

        if filter_completed is True:
            print(f"{Colors.HEADER}║{Colors.BOLD}                        COMPLETED TASKS                                {Colors.ENDC}{Colors.HEADER}║{Colors.ENDC}")
        elif filter_completed is False:
            print(f"{Colors.HEADER}║{Colors.BOLD}                        PENDING TASKS                                  {Colors.ENDC}{Colors.HEADER}║{Colors.ENDC}")
        else:
            print(f"{Colors.HEADER}║{Colors.BOLD}                         ALL TASKS                                     {Colors.ENDC}{Colors.HEADER}║{Colors.ENDC}")

        print(f"{Colors.HEADER}╚" + "═" * 78 + "╝{Colors.ENDC}")

        todos = self.app.list_todos(filter_completed)

        if not todos:
            if filter_completed is True:
                print(f"   {Colors.WARNING}No completed tasks found.{Colors.ENDC}")
            elif filter_completed is False:
                print(f"   {Colors.WARNING}No pending tasks found.{Colors.ENDC}")
            else:
                print(f"   {Colors.WARNING}No tasks found.{Colors.ENDC}")
            return

        print(f"   {Colors.BOLD}Total Tasks: {len(todos)}{Colors.ENDC}")
        print(f"   {'─' * 70}")

        for i, todo in enumerate(todos, 1):
            print(f"   {i}. {todo}")
            print()

    def update_task(self):
        """Update an existing task with clear guidance."""
        print(f"\n{Colors.HEADER}╔" + "═" * 78 + "╗{Colors.ENDC}")
        print(f"{Colors.HEADER}║{Colors.BOLD}                        UPDATE TASK                                      {Colors.ENDC}{Colors.HEADER}║{Colors.ENDC}")
        print(f"{Colors.HEADER}╚" + "═" * 78 + "╝{Colors.ENDC}")

        try:
            if not self.app.list_todos():
                print(f"   {Colors.WARNING}No tasks available to update.{Colors.ENDC}")
                return

            print(f"   {Colors.BOLD}Current tasks:{Colors.ENDC}")
            for todo in self.app.list_todos():
                status = "✓" if todo.completed else "○"
                print(f"      [{status}] ID: {todo.id} - {todo.title}")

            task_id = int(input(f"\n   Enter task ID to update: ").strip())

            if not self.app.get_todo(task_id):
                print(f"   {Colors.FAIL}❌ ERROR: Task with ID {task_id} not found!{Colors.ENDC}")
                return

            todo = self.app.get_todo(task_id)
            print(f"\n   {Colors.BOLD}Current task details:{Colors.ENDC}")
            print(f"      ID: {todo.id}")
            print(f"      Title: {todo.title}")
            print(f"      Description: {todo.description if todo.description else 'None'}")
            print(f"      Status: {'Completed' if todo.completed else 'Pending'}")

            print(f"\n   {Colors.BOLD}Enter new details (press Enter to keep current):{Colors.ENDC}")
            new_title = input(f"      New title (current: '{todo.title}'): ").strip()
            new_title = new_title if new_title else None

            new_description = input(f"      New description (current: '{todo.description if todo.description else 'None'}'): ").strip()
            new_description = new_description if new_description else None

            if new_title is None and new_description is None:
                print(f"   {Colors.WARNING}No changes made.{Colors.ENDC}")
                return

            if self.app.update_todo(task_id, new_title, new_description):
                print(f"   {Colors.OKGREEN}✅ SUCCESS: Task updated successfully!{Colors.ENDC}")
            else:
                print(f"   {Colors.FAIL}❌ ERROR: Failed to update task!{Colors.ENDC}")

        except ValueError:
            print(f"   {Colors.FAIL}❌ ERROR: Please enter a valid task ID (number)!{Colors.ENDC}")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Colors.WARNING}   Operation cancelled.{Colors.ENDC}")

    def delete_task(self):
        """Delete a task with confirmation."""
        print(f"\n{Colors.HEADER}╔" + "═" * 78 + "╗{Colors.ENDC}")
        print(f"{Colors.HEADER}║{Colors.BOLD}                        DELETE TASK                                      {Colors.ENDC}{Colors.HEADER}║{Colors.ENDC}")
        print(f"{Colors.HEADER}╚" + "═" * 78 + "╝{Colors.ENDC}")

        try:
            if not self.app.list_todos():
                print(f"   {Colors.WARNING}No tasks available to delete.{Colors.ENDC}")
                return

            print(f"   {Colors.BOLD}Current tasks:{Colors.ENDC}")
            for todo in self.app.list_todos():
                status = "✓" if todo.completed else "○"
                print(f"      [{status}] ID: {todo.id} - {todo.title}")

            task_id = int(input(f"\n   Enter task ID to delete: ").strip())

            if not self.app.get_todo(task_id):
                print(f"   {Colors.FAIL}❌ ERROR: Task with ID {task_id} not found!{Colors.ENDC}")
                return

            # Confirmation
            confirm = input(f"   {Colors.WARNING}Are you sure you want to delete task ID {task_id}? (y/N): {Colors.ENDC}").strip().lower()

            if confirm in ['y', 'yes']:
                if self.app.delete_todo(task_id):
                    print(f"   {Colors.OKGREEN}✅ SUCCESS: Task deleted successfully!{Colors.ENDC}")
                else:
                    print(f"   {Colors.FAIL}❌ ERROR: Failed to delete task!{Colors.ENDC}")
            else:
                print(f"   {Colors.WARNING}Delete operation cancelled.{Colors.ENDC}")

        except ValueError:
            print(f"   {Colors.FAIL}❌ ERROR: Please enter a valid task ID (number)!{Colors.ENDC}")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Colors.WARNING}   Operation cancelled.{Colors.ENDC}")

    def toggle_task_completion(self):
        """Toggle task completion with clear feedback."""
        print(f"\n{Colors.HEADER}╔" + "═" * 78 + "╗{Colors.ENDC}")
        print(f"{Colors.HEADER}║{Colors.BOLD}                   MARK TASK COMPLETE/INCOMPLETE                           {Colors.ENDC}{Colors.HEADER}║{Colors.ENDC}")
        print(f"{Colors.HEADER}╚" + "═" * 78 + "╝{Colors.ENDC}")

        try:
            if not self.app.list_todos():
                print(f"   {Colors.WARNING}No tasks available to update.{Colors.ENDC}")
                return

            print(f"   {Colors.BOLD}Current tasks:{Colors.ENDC}")
            for todo in self.app.list_todos():
                status = "✓" if todo.completed else "○"
                print(f"      [{status}] ID: {todo.id} - {todo.title}")

            task_id = int(input(f"\n   Enter task ID to toggle completion: ").strip())

            if not self.app.get_todo(task_id):
                print(f"   {Colors.FAIL}❌ ERROR: Task with ID {task_id} not found!{Colors.ENDC}")
                return

            if self.app.toggle_completion(task_id):
                todo = self.app.get_todo(task_id)
                status = f"{Colors.OKGREEN}COMPLETED{Colors.ENDC}" if todo.completed else f"{Colors.WARNING}PENDING{Colors.ENDC}"
                print(f"   {Colors.OKGREEN}✅ SUCCESS: Task marked as {status}!{Colors.ENDC}")
            else:
                print(f"   {Colors.FAIL}❌ ERROR: Failed to update task!{Colors.ENDC}")

        except ValueError:
            print(f"   {Colors.FAIL}❌ ERROR: Please enter a valid task ID (number)!{Colors.ENDC}")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Colors.WARNING}   Operation cancelled.{Colors.ENDC}")

    def show_statistics(self):
        """Show detailed statistics with professional formatting."""
        print(f"\n{Colors.HEADER}╔" + "═" * 78 + "╗{Colors.ENDC}")
        print(f"{Colors.HEADER}║{Colors.BOLD}                      DETAILED STATISTICS                                {Colors.ENDC}{Colors.HEADER}║{Colors.ENDC}")
        print(f"{Colors.HEADER}╚" + "═" * 78 + "╝{Colors.ENDC}")

        stats = self.app.get_statistics()

        print(f"   {Colors.BOLD}📊 DETAILED BREAKDOWN:{Colors.ENDC}")
        print(f"   ┌─────────────────────┬─────────────┐")
        print(f"   │ Metric              │ Count       │")
        print(f"   ├─────────────────────┼─────────────┤")
        print(f"   │ Total Tasks         │ {stats['total']:>10} │")
        print(f"   │ Completed Tasks     │ {stats['completed']:>10} │")
        print(f"   │ Pending Tasks       │ {stats['pending']:>10} │")
        print(f"   └─────────────────────┴─────────────┘")

        if stats['total'] > 0:
            print(f"\n   {Colors.BOLD}📈 PROGRESS ANALYSIS:{Colors.ENDC}")
            completion_bar = "█" * int(stats['completion_percentage'] // 5)
            empty_bar = "░" * (20 - len(completion_bar))
            print(f"   Completion Rate: [{Colors.OKGREEN}{completion_bar}{Colors.ENDC}{empty_bar}] {Colors.OKGREEN if stats['completion_percentage'] >= 50 else Colors.WARNING}{stats['completion_percentage']:.1f}%{Colors.ENDC}")

            print(f"\n   {Colors.BOLD}📋 PERFORMANCE:{Colors.ENDC}")
            if stats['completion_percentage'] >= 100:
                print(f"      🏆 EXCELLENT: All tasks completed!")
            elif stats['completion_percentage'] >= 75:
                print(f"      🌟 GREAT: Excellent progress!")
            elif stats['completion_percentage'] >= 50:
                print(f"      👍 GOOD: Halfway to your goal!")
            elif stats['completion_percentage'] > 0:
                print(f"      💪 FAIR: Making steady progress!")
            else:
                print(f"      🚀 START: Time to begin working!")

            print(f"\n   {Colors.BOLD}💡 RECOMMENDATION:{Colors.ENDC}")
            if stats['pending'] > 5:
                print(f"      You have many pending tasks. Consider prioritizing them.")
            elif stats['pending'] > 0:
                print(f"      You have some pending tasks. Keep working!")
            else:
                print(f"      Well done! All tasks are completed.")

    def run(self):
        """Run the main application with professional flow."""
        print(f"{Colors.OKGREEN}🎉 WELCOME TO PROFESSIONAL TODO APPLICATION!{Colors.ENDC}")
        print(f"{Colors.WARNING}💡 INFO: All data is stored in memory only and will be lost when you exit.{Colors.ENDC}")
        print(f"{Colors.OKBLUE}📋 TIP: Use this app to organize and track your daily tasks efficiently.{Colors.ENDC}")

        while True:
            self.display_header()
            self.display_statistics()
            self.display_menu()

            choice = self.get_user_choice()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.view_tasks(filter_completed=True)
            elif choice == "4":
                self.view_tasks(filter_completed=False)
            elif choice == "5":
                self.update_task()
            elif choice == "6":
                self.delete_task()
            elif choice == "7":
                self.toggle_task_completion()
            elif choice == "8":
                self.show_statistics()
            elif choice == "9":
                print(f"\n{Colors.WARNING}👋 Thank you for using Professional Todo Application!{Colors.ENDC}")
                print(f"{Colors.WARNING}📋 Your data was stored in memory only and has been cleared.{Colors.ENDC}")
                print(f"{Colors.WARNING}👋 Goodbye! Have a productive day!{Colors.ENDC}")
                break
            else:
                print(f"{Colors.FAIL}❌ INVALID CHOICE: Please enter a number between 1-9.{Colors.ENDC}")

            # Pause to let user see the result
            if choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                input(f"\n{Colors.OKBLUE}Press Enter to continue to main menu...{Colors.ENDC}")


def main():
    """Main entry point."""
    interface = TodoConsoleInterface()
    interface.run()


if __name__ == "__main__":
    main()