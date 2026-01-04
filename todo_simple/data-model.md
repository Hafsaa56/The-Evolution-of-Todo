# Data Model - Simple Todo Console Application

## Entities

### Todo Entity
- **id**: Integer
  - Unique identifier
  - Auto-incremented
  - Primary key
- **title**: String
  - Required field
  - Non-empty after trimming whitespace
  - Maximum length: No explicit limit
- **description**: String (Optional)
  - Optional field
  - Can be empty
  - Maximum length: No explicit limit
- **completed**: Boolean
  - Status indicator
  - Default value: False

## Storage Model
- **Type**: Dictionary/Map
- **Key**: Integer (Todo.id)
- **Value**: Todo object
- **Access pattern**: Direct key lookup O(1)
- **Constraints**:
  - Unique keys (enforced by dictionary structure)
  - No concurrent access (synchronous application)

## State Transitions
- **New Todo**: created with completed=False
- **Update**: title and/or description can be modified
- **Toggle Completion**: completed status flips between True/False
- **Delete**: Todo removed from storage entirely
- **Persistence**: Data exists only in memory; lost on application exit