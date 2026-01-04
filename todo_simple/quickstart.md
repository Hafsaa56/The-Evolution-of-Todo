# Quickstart Guide - Simple Todo Console Application

## Prerequisites
- Python 3.6 or higher
- No external libraries required

## Running the Application
1. Navigate to the project directory
2. Run the application:
   ```bash
   python todo_simple/todo_app.py
   ```

## Basic Usage
1. The application will display a main menu with numbered options
2. Enter the number of the option you want to select
3. Follow the prompts to provide required information
4. The application will confirm all successful operations

## Available Operations
1. **Add a new task**: Create a new todo with title and optional description
2. **View all tasks**: Display all existing todos with their status
3. **Update an existing task**: Modify title or description of an existing todo
4. **Delete a task**: Remove a todo from memory
5. **Mark a task as complete/incomplete**: Toggle the completion status of a todo
6. **Exit**: Quit the application (all data will be lost)

## Example Workflow
1. Add a task: Select option 1, enter "Buy groceries" as title
2. View tasks: Select option 2 to see your task list
3. Complete task: Select option 5, enter the task ID to mark as complete
4. Exit: Select option 6 to quit the application

## Error Handling
- Invalid inputs will show error messages
- Non-existent task IDs will show appropriate error messages
- Empty titles will be rejected when adding/updating tasks