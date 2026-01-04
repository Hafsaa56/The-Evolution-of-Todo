# Full-Stack Todo Application

A full-stack web application with user authentication and task management capabilities.

## Features

- User registration and login with JWT authentication
- Secure task management with CRUD operations
- Multi-user support with data isolation
- Responsive web interface

## Tech Stack

### Backend
- FastAPI - Web framework
- SQLModel - Database ORM
- Neon PostgreSQL - Database
- JWT - Authentication

### Frontend
- Next.js - React framework with App Router
- Tailwind CSS - Styling

## Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

5. Run the application:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API configuration
```

4. Run the development server:
```bash
npm run dev
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user profile

### Tasks
- `GET /tasks` - Get user's tasks
- `POST /tasks` - Create new task
- `GET /tasks/{id}` - Get specific task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `PATCH /tasks/{id}/toggle` - Toggle task completion

### Health Check
- `GET /health` - Check API health status

## Environment Variables

### Backend (.env)
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing key
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time

### Frontend (.env)
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NEXT_PUBLIC_APP_NAME` - Application name

## Development

Backend runs on http://localhost:8000 by default.
Frontend runs on http://localhost:3000 by default.

API documentation is available at http://localhost:8000/docs when running the backend.

## Deployment

### Docker Deployment

To deploy the application using Docker:

1. Make sure you have Docker and Docker Compose installed.

2. Create environment files with your configuration:
   ```bash
   # In the backend directory
   cp .env.example .env
   # Edit backend/.env with your database credentials and secret key

   # In the frontend directory
   cp .env.example .env
   # Edit frontend/.env with your API configuration
   ```

3. Run the application: !
   ```bash
   docker-compose up --build
   ```

The application will be available at http://localhost:3000.