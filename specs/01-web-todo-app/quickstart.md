# Quickstart Guide - Phase II Full-Stack Web Todo Application

## Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL (or Neon PostgreSQL account)
- Git

## Project Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API configuration
```

## Database Setup

### 1. Configure Neon PostgreSQL
- Create a Neon PostgreSQL account
- Create a new project
- Copy the connection string to your .env file

### 2. Run Database Migrations
```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

## Running the Application

### 1. Start Backend Server
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### 2. Start Frontend Server
```bash
cd frontend
npm run dev
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout user

### Tasks
- `GET /tasks` - Get all user's tasks
- `POST /tasks` - Create new task
- `GET /tasks/{id}` - Get specific task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `PATCH /tasks/{id}/toggle` - Toggle task completion

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

### Backend Development
- Backend runs on http://localhost:8000 by default
- API documentation available at http://localhost:8000/docs
- Use FastAPI's built-in validation and type hints

### Frontend Development
- Frontend runs on http://localhost:3000 by default
- Uses Next.js App Router
- API integration through axios/fetch clients

## Testing

### Backend Tests
```bash
cd backend
python -m pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Building for Production

### Backend
```bash
cd backend
pip install -r requirements.txt
# Deploy with your preferred WSGI/ASGI server
```

### Frontend
```bash
cd frontend
npm run build
# Serve the built application with your preferred server
```

## Troubleshooting

### Common Issues
- Make sure database credentials are correctly configured
- Ensure both backend and frontend servers are running
- Check that CORS settings allow communication between frontend and backend
- Verify JWT token is properly included in authorization headers