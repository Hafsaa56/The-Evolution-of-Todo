# Simple Todo Console Application

A simple, synchronous todo application that runs in the terminal with menu-based interaction. All data exists only in memory and is lost when the program exits.

## Features

- Add new tasks with title and optional description
- View all tasks with completion status
- Update existing tasks
- Delete tasks
- Mark tasks as complete or incomplete

## Requirements

- Python 3.6 or higher
- No external libraries required

## Usage

Run the application:

```bash
python todo_simple/todo_app.py
```

Follow the menu prompts to interact with the application:

1. **Add a new task**: Enter title and optional description
2. **View all tasks**: Display all tasks with completion status
3. **Update an existing task**: Modify title or description
4. **Delete a task**: Remove a task by ID
5. **Mark a task as complete/incomplete**: Toggle completion status
6. **Exit**: Quit the application

## Data Model

Each task contains:
- ID (unique integer, auto-increment)
- Title (string, required)
- Description (string, optional)
- Completed (boolean, default false)

## Architecture

This is a simple synchronous application with no external dependencies:
- `Todo` class: Represents a single todo item
- `TodoApp` class: Handles business logic and data storage
- `TodoConsoleInterface` class: Handles user interaction
- All data is stored in memory and lost when program exits

## Constraints

- Python only, no external libraries
- No async or threading
- Menu-based interaction via terminal prompts
- In-memory storage only