# Phase I Specification — In-Memory Todo Console App

## Objective
Build a simple, reliable, single-user Todo application running in the terminal.
The application must store all data in memory and terminate cleanly.

## Functional Requirements
The system MUST support:
1. Add a new task
2. View all tasks
3. Update an existing task
4. Delete a task
5. Mark a task as complete or incomplete

## Task Model
Each task MUST contain:
- id (unique integer, auto-increment)
- title (string, required)
- description (string, optional)
- completed (boolean, default false)

## User Interaction
- Interaction MUST be via terminal prompts
- User MUST choose actions via a menu
- Clear success and error messages MUST be shown

## Persistence Rules
- Data MUST exist only in memory
- When program exits, all data is lost

## Constraints
- Python only
- No database
- No external libraries
- No async or threading
- No web framework
- No AI features

## Output
- A runnable Python CLI application
- Clean folder structure
- Readable, maintainable code

This specification is binding.

## User Scenarios & Testing

### Scenario 1: Adding a new task
- User starts the application
- User selects "Add a new task" from the menu
- User enters a title and optional description
- System validates the input
- System creates and stores the new task
- System displays success message with the task ID

### Scenario 2: Viewing all tasks
- User starts the application with existing tasks
- User selects "View all tasks" from the menu
- System displays all tasks with their ID, title, description, and completion status
- System shows appropriate message if no tasks exist

### Scenario 3: Updating an existing task
- User starts the application with existing tasks
- User selects "Update an existing task" from the menu
- User enters the task ID to update
- System validates the task exists
- User enters new title and/or description
- System updates the task
- System displays success message

### Scenario 4: Deleting a task
- User starts the application with existing tasks
- User selects "Delete a task" from the menu
- User enters the task ID to delete
- System validates the task exists
- System removes the task from memory
- System displays success message

### Scenario 5: Marking a task as complete/incomplete
- User starts the application with existing tasks
- User selects "Mark a task as complete/incomplete" from the menu
- User enters the task ID to toggle
- System validates the task exists
- System toggles the completion status
- System displays success message with new status

## Success Criteria

- 100% of user tasks can be completed through the menu interface without errors
- Response time for all operations is under 1 second
- 95% of users can successfully add, view, update, delete, and toggle tasks without assistance
- Application handles invalid inputs gracefully with clear error messages
- All data remains in memory during application lifecycle
- All data is completely lost when application exits

## Key Entities

- **Todo**: Represents a single task with id, title, description, and completion status
- **TodoApp**: Core application logic for managing todos
- **TodoConsoleInterface**: Handles user interaction through terminal menu

## Assumptions

- User has access to a Python 3.6+ environment
- User is familiar with basic terminal interaction
- Application runs in a single-user environment
- Data persistence is not required beyond application lifecycle
- No concurrent access to the application