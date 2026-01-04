# Phase II Specification — Full-Stack Web Todo Application

## Objective
Evolve the Phase-I console Todo application into a secure,
multi-user, full-stack web application with persistent storage.

## Functional Requirements
The system MUST support:
1. User registration and login
2. JWT-based authentication
3. Add, view, update, delete Todo tasks
4. Mark tasks as complete or incomplete
5. Each user can access ONLY their own tasks

## Task Model
Each task MUST contain:
- id (UUID or integer)
- user_id (foreign key)
- title (string, required)
- description (string, optional)
- completed (boolean, default false)
- created_at (timestamp)

## User Model
Each user MUST contain:
- id
- email (unique)
- hashed_password
- created_at

## Architecture
- Frontend: Next.js (App Router)
- Backend: FastAPI
- Database: Neon Serverless PostgreSQL
- ORM: SQLModel
- Auth: JWT (Better Auth compatible)

## Constraints
- Python backend only
- No AI features
- No Docker or Kubernetes
- REST APIs only (no GraphQL)
- Secure password hashing

## Output
- Working full-stack application
- Persistent storage
- Clean API contracts
- Proper error handling

This specification is binding.

## User Scenarios & Testing

### Scenario 1: User Registration
- User navigates to registration page
- User enters email and password
- System validates input and creates new user account
- System returns success response with authentication token

### Scenario 2: User Login
- User navigates to login page
- User enters registered email and password
- System validates credentials and returns JWT token
- User is authenticated for subsequent requests

### Scenario 3: Create Todo Task
- Authenticated user creates a new task
- System validates input and creates task associated with user's account
- System returns created task data

### Scenario 4: View User's Tasks
- Authenticated user requests their tasks
- System returns only tasks belonging to the authenticated user
- Tasks are displayed with completion status

### Scenario 5: Update Task
- Authenticated user updates one of their tasks
- System validates that user owns the task
- System updates the task and returns updated data

### Scenario 6: Delete Task
- Authenticated user deletes one of their tasks
- System validates that user owns the task
- System deletes the task and confirms deletion

### Scenario 7: Toggle Task Completion
- Authenticated user marks a task as complete/incomplete
- System validates that user owns the task
- System updates completion status and returns updated task

## Success Criteria

- 100% of users can successfully register and login to the application
- 95% of registered users can create, view, update, and delete their own tasks
- System properly enforces access control so users can only access their own tasks
- Authentication tokens are securely generated and validated
- Passwords are securely hashed using industry-standard algorithms
- Application handles invalid inputs gracefully with clear error messages
- System maintains data integrity and consistency across all operations

## Key Entities

- **User**: Represents a registered user with authentication credentials
- **Task**: Represents a todo item associated with a specific user
- **Authentication**: Manages user sessions and access control via JWT tokens
- **Database**: Persistent storage for users and tasks using PostgreSQL

## Assumptions

- Users have access to a modern web browser
- Database connection is available for persistent storage
- Authentication tokens are stored securely on the client side
- Network connectivity is available for web application access
- Application follows security best practices for web applications