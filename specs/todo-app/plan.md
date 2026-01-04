# Todo App Implementation Plan

## 1. Architecture Overview

### 1.1 Clean Architecture Layers
- **Presentation Layer**: CLI interface handling user input/output
- **Application Layer**: Business logic and use cases
- **Domain Layer**: Core entities and interfaces
- **Infrastructure Layer**: Data persistence and external services

### 1.2 Technology Stack
- **Language**: Python 3.9+
- **Framework**: FastAPI (for later phases)
- **Database**: SQLModel with Neon PostgreSQL
- **CLI**: Standard library argparse
- **Testing**: pytest
- **Serialization**: Pydantic models

## 2. Phase I Implementation (In-Memory CLI)

### 2.1 Domain Layer
- Define Todo entity with ID, title, description, status, timestamps
- Define TodoRepository interface
- Define use case interfaces

### 2.2 Application Layer
- Implement AddTodo use case
- Implement ListTodos use case
- Implement CompleteTodo use case
- Implement DeleteTodo use case
- Implement EditTodo use case
- Implement FilterTodos use case

### 2.3 Infrastructure Layer
- Implement InMemoryTodoRepository
- Implement FileTodoRepository (for later persistence)

### 2.4 Presentation Layer
- Implement CLI with argparse
- Implement command handlers
- Implement output formatters (human-readable and JSON)

## 3. Detailed Implementation Steps

### 3.1 Domain Layer Implementation
1. Create Todo data model with Pydantic
2. Define TodoStatus enum (ACTIVE, COMPLETED)
3. Define TodoRepository protocol with CRUD operations
4. Define use case input/output models

### 3.2 Application Layer Implementation
1. Implement AddTodo use case with validation
2. Implement ListTodos use case with filtering
3. Implement CompleteTodo use case with validation
4. Implement DeleteTodo use case with validation
5. Implement EditTodo use case with validation
6. Implement FilterTodos use case with status filtering

### 3.3 Infrastructure Layer Implementation
1. Implement InMemoryTodoRepository with thread-safe operations
2. Implement FileTodoRepository for file-based persistence
3. Implement DatabaseTodoRepository for PostgreSQL (Phase III)

### 3.4 Presentation Layer Implementation
1. Create CLI entry point with argparse
2. Implement add command handler
3. Implement list command handler
4. Implement complete command handler
5. Implement delete command handler
6. Implement edit command handler
7. Implement filter command handler
8. Implement output formatters

## 4. Data Models

### 4.1 Todo Entity
- id: UUID (auto-generated)
- title: str (required, min length 1)
- description: Optional[str]
- status: TodoStatus (ACTIVE/COMPLETED)
- created_at: datetime (auto-generated)
- updated_at: datetime (auto-generated, updated on change)

### 4.2 Input/Output Models
- CreateTodoRequest: title, description
- UpdateTodoRequest: title, description, status
- TodoResponse: all fields for API responses

## 5. CLI Commands Structure
```
todo add --title "Task title" --description "Task description"
todo list [--status all|active|completed]
todo complete <id>
todo delete <id>
todo edit <id> --title "New title" --description "New description"
todo filter --status active|completed
```

## 6. Error Handling
- Define application-specific exceptions
- Implement proper error codes
- Provide meaningful error messages
- Handle validation errors

## 7. Testing Strategy
- Unit tests for domain entities
- Unit tests for use cases
- Integration tests for repository implementations
- CLI command tests
- End-to-end tests

## 8. Phase Evolution Plan

### Phase I (Current) - CLI with In-Memory Storage
- [ ] Basic CLI application
- [ ] In-memory repository
- [ ] Core CRUD operations
- [ ] Basic error handling
- [ ] Unit tests

### Phase II - File-Based Persistence
- [ ] File-based repository
- [ ] Data serialization/deserialization
- [ ] Data migration between formats

### Phase III - Database Integration
- [ ] SQLModel entities
- [ ] Database repository implementation
- [ ] Connection pooling
- [ ] Transaction management

### Phase IV - Web API
- [ ] FastAPI endpoints
- [ ] Request/response validation
- [ ] Authentication/authorization
- [ ] API documentation

### Phase V - Distributed System
- [ ] Dapr integration
- [ ] Event-driven architecture
- [ ] Message queues (Kafka)
- [ ] Kubernetes deployment