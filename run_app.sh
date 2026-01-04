#!/bin/bash

# Script to run the full-stack Todo application

echo "Starting the Todo Application..."

# Function to start backend
start_backend() {
    echo "Starting backend server..."
    cd backend
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    else
        echo "Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    fi

    # Check if .env file exists, if not create it
    if [ ! -f ".env" ]; then
        echo "Creating backend .env file..."
        cp .env.example .env
        # Generate a random secret key
        SECRET_KEY=$(openssl rand -hex 32)
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    fi

    uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    cd ..
}

# Function to start frontend
start_frontend() {
    echo "Starting frontend server..."
    cd frontend

    # Check if node_modules exists, if not install dependencies
    if [ ! -d "node_modules" ]; then
        echo "Installing frontend dependencies..."
        npm install
    fi

    # Check if .env file exists, if not create it
    if [ ! -f ".env" ]; then
        echo "Creating frontend .env file..."
        cp .env.example .env
    fi

    npm run dev &
    FRONTEND_PID=$!
    cd ..
}

# Start both servers
start_backend
sleep 5  # Wait for backend to start
start_frontend

echo "Applications are running!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the applications"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID