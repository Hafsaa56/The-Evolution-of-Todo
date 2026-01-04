# Data Model - Phase II Full-Stack Web Todo Application

## Entities

### User Entity
- **id**: UUID
  - Primary key
  - Auto-generated using UUID4
  - Unique identifier for each user
- **email**: String
  - Required field
  - Unique constraint
  - Must be valid email format
  - Maximum length: 255 characters
- **hashed_password**: String
  - Required field
  - Stored as bcrypt hash
  - Maximum length: 255 characters
- **created_at**: DateTime
  - Auto-generated timestamp
  - Records when user account was created
- **updated_at**: DateTime
  - Auto-generated timestamp
  - Updated when user record is modified

### Task Entity
- **id**: UUID
  - Primary key
  - Auto-generated using UUID4
  - Unique identifier for each task
- **user_id**: UUID
  - Foreign key to User entity
  - Required field
  - Establishes ownership relationship
- **title**: String
  - Required field
  - Minimum length: 1 character
  - Maximum length: 255 characters
- **description**: String (Optional)
  - Optional field
  - Maximum length: 1000 characters
- **completed**: Boolean
  - Status indicator
  - Default value: False
- **created_at**: DateTime
  - Auto-generated timestamp
  - Records when task was created
- **updated_at**: DateTime
  - Auto-generated timestamp
  - Updated when task is modified

## Relationships
- **User to Tasks**: One-to-Many
  - One user can have multiple tasks
  - Each task belongs to exactly one user
  - Foreign key constraint on Task.user_id
  - Cascade delete: When user is deleted, all their tasks are deleted

## Constraints
- **User**:
  - Email must be unique
  - Email must match email format validation
  - Password must be securely hashed (not stored in plain text)
- **Task**:
  - User_id must reference an existing user
  - Title must be provided (not empty)
  - User can only access their own tasks

## Indexes
- **User**:
  - Index on email field (for authentication queries)
- **Task**:
  - Index on user_id field (for user-specific queries)
  - Index on completed field (for filtering queries)

## Validation Rules
- **User Creation**:
  - Email must be valid format
  - Email must not already exist
  - Password must be provided and hashed
- **Task Creation**:
  - Title must be provided and not empty
  - User must be authenticated
  - User can only create tasks for themselves
- **Task Access**:
  - Users can only access tasks they own
  - Authentication required for all task operations