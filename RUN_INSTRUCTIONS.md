# Todo Application - Running Instructions

This document provides step-by-step instructions on how to run the full-stack Todo application with user authentication and task management.

## Prerequisites

Before running the application, make sure you have the following installed on your system:

- **Python 3.8+** (for the backend)
- **Node.js 18+** (for the frontend)
- **npm** (usually comes with Node.js)
- **pip** (Python package manager)
- **git** (optional, for cloning if needed)

## Quick Start (Recommended)

### Using the Run Scripts

We've provided convenient scripts to run the application:

#### On Windows:
1. Double-click the `run_app.bat` file, OR
2. Open Command Prompt as Administrator in this folder and run:
```cmd
run_app.bat
```

#### On Linux/Mac:
1. Open terminal in this folder and run:
```bash
./run_app.sh
```

## Manual Setup (Step-by-step)

### 1. Backend Setup (Python/FastAPI)

1. **Open a terminal/command prompt** and navigate to the backend directory:
```bash
cd backend
```

2. **Create a virtual environment** (optional but recommended):
```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On Linux/Mac:
python3 -m venv venv
source venv/bin/activate
```

3. **Install backend dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file to set your configuration
```
Edit the `.env` file to set:
- `DATABASE_URL`: Your PostgreSQL database URL (default: `postgresql://user:password@localhost:5432/todo_app`)
- `SECRET_KEY`: A random secret key for JWT tokens
- `ALGORITHM`: Default is `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Default is `30`

5. **Run the backend server**:
```bash
uvicorn main:app --reload
```

The backend will start on `http://localhost:8000`

### 2. Frontend Setup (React/Next.js)

1. **Open a new terminal/command prompt** and navigate to the frontend directory:
```bash
cd frontend  # from the main project directory
```

2. **Install frontend dependencies**:
```bash
npm install
```

3. **Set up environment variables**:
```bash
# Copy the example environment file
cp .env.example .env
```

Edit the `.env` file to set:
- `NEXT_PUBLIC_API_URL`: Should be `http://localhost:8000` (where backend is running)
- `NEXT_PUBLIC_APP_NAME`: Your app name (default: `Todo App`)

4. **Run the frontend development server**:
```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

## Running Both Servers Together

You need both servers running simultaneously:
1. Start the backend server first
2. Wait about 5-10 seconds for it to initialize
3. Start the frontend server in a separate terminal

## Accessing the Application

Once both servers are running:

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Using the Application

1. Open your browser and go to `http://localhost:3000`
2. You'll see the welcome page with options to register or login
3. Click "Create account" to register a new user, or "Sign in" if you have an account
4. After registration/login, you'll be redirected to the dashboard
5. On the dashboard, you can:
   - Create new tasks
   - View existing tasks
   - Edit tasks
   - Mark tasks as complete/incomplete
   - Delete tasks
   - Log out

## Troubleshooting

### Common Issues:

1. **Port already in use**:
   - Make sure no other applications are using ports 8000 or 3000
   - Close other applications or change the port numbers in the run commands

2. **Database connection issues**:
   - Make sure you have PostgreSQL installed and running
   - Verify your `DATABASE_URL` in the backend `.env` file

3. **Dependencies not installed**:
   - Make sure to run `pip install -r requirements.txt` in the backend
   - Make sure to run `npm install` in the frontend

4. **Environment variables missing**:
   - Make sure to create and configure both `.env` files

### If you encounter any issues:

1. Check the terminal output for error messages
2. Verify that both servers are running
3. Make sure the API URLs are correctly configured
4. Restart both servers if needed

## Stopping the Application

To stop the servers:
- Press `Ctrl+C` in each terminal where the servers are running
- Close the terminal windows

## Additional Information

- The backend automatically creates database tables on startup
- User passwords are securely hashed using bcrypt
- JWT tokens are used for authentication
- Each user can only access their own tasks
- The application is responsive and works on mobile devices