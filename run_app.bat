@echo off
echo Starting the Todo Application...

REM Function to start backend
:start_backend
echo Starting backend server...
cd backend

REM Check if virtual environment exists, if not create it
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies if not already installed
if not exist "venv\Lib\site-packages\fastapi" (
    echo Installing backend dependencies...
    pip install -r requirements.txt
)

REM Check if .env file exists, if not create it
if not exist ".env" (
    echo Creating backend .env file...
    copy .env.example .env
)

REM Start backend server
start cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"
cd ..

REM Wait a bit for backend to start
timeout /t 5 /nobreak >nul

REM Function to start frontend
:start_frontend
echo Starting frontend server...
cd frontend

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo Installing frontend dependencies...
    npm install
)

REM Check if .env file exists, if not create it
if not exist ".env" (
    echo Creating frontend .env file...
    copy .env.example .env
)

REM Start frontend server
start cmd /k "npm run dev"
cd ..

echo Applications are running!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Documentation: http://localhost:8000/docs
echo.
echo Servers started in separate command prompts.

pause