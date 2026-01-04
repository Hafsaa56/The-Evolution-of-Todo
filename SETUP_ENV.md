# Environment Setup Guide

This guide explains how to set up the environment variables for the Todo application.

## Backend Environment Variables (.env file)

### Location: `/backend/.env`

### Required Variables:
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### How to generate a SECRET_KEY:
1. Using Python (in Python terminal or script):
```python
import secrets
print(secrets.token_urlsafe(32))
```

2. Or using command line (Linux/Mac):
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

3. For development only, you can use any random string, e.g.:
```
SECRET_KEY=mydevsecretkeythatshouldbeverylongandrandom123456
```

### Example .env file:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/todo_app
SECRET_KEY=very-long-random-secret-key-generated-using-python-secrets
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Frontend Environment Variables (.env file)

### Location: `/frontend/.env`

### Required Variables:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Todo App
BACKEND_API_URL=http://localhost:8000
```

### For Development:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Todo App
BACKEND_API_URL=http://localhost:8000
```

### For Production (example):
```
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
NEXT_PUBLIC_APP_NAME=Todo App
BACKEND_API_URL=https://yourdomain.com/api
```

## Quick Setup Steps:

### 1. Backend Setup:
```bash
# Navigate to backend
cd backend

# Copy example file
cp .env.example .env

# Edit the .env file with your values
```

### 2. Frontend Setup:
```bash
# Navigate to frontend
cd frontend

# Copy example file
cp .env.example .env

# Edit the .env file with your values
```

## Database Setup (PostgreSQL):

### Option 1: Local PostgreSQL
1. Install PostgreSQL on your system
2. Create a database named `todo_app`
3. Update DATABASE_URL in backend/.env

### Option 2: Using Docker for PostgreSQL
```bash
# Run PostgreSQL in Docker
docker run --name todo-postgres -e POSTGRES_DB=todo_app -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15
```

### Option 3: Using Neon (Cloud PostgreSQL - Recommended for development)
1. Go to https://neon.tech/
2. Create a free account
3. Create a new project
4. Get the connection string and use it as DATABASE_URL

## Default Configuration (Works for Development):

### Backend (.env):
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/todo_app
SECRET_KEY=dev-secret-key-for-testing-purposes-only
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Todo App
BACKEND_API_URL=http://localhost:8000
```

## Troubleshooting Environment Issues:

### Common Problems:
1. **Backend can't connect to database**: Check DATABASE_URL
2. **Authentication fails**: Check SECRET_KEY is the same for token generation/verification
3. **Frontend can't reach backend**: Check NEXT_PUBLIC_API_URL matches backend URL

### Quick Fixes:
- Make sure backend is running before frontend
- Verify port numbers (8000 for backend, 3000 for frontend)
- Check that URLs use correct protocol (http:// or https://)
- Ensure no special characters in passwords without proper escaping

## Security Notes:
- Never commit .env files to version control
- Use strong, random SECRET_KEY in production
- Use different SECRET_KEY for different environments
- Consider using environment-specific .env files (e.g., .env.development, .env.production)