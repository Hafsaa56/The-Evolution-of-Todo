#!/bin/bash
set -e  # Exit on any error

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt --force-reinstall --no-cache-dir

echo "Setting up environment variables..."
export DATABASE_URL="sqlite:///./todo_app.db"
export SECRET_KEY="${SECRET_KEY:-your-super-secret-key-change-this}"
export ALGORITHM="HS256"
export ACCESS_TOKEN_EXPIRE_MINUTES="30"

echo "Starting application on port: $PORT"
if [ -z "$PORT" ]; then
    echo "PORT environment variable not set, using default 8000"
    export PORT=8000
fi

cd backend
echo "Running database migrations and starting server..."
python -c "
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sqlmodel import SQLModel
from database import engine
from main import app
from database import on_startup
on_startup()
print('Database tables created successfully')
"

python -m uvicorn main:app --host=0.0.0.0 --port=$PORT --timeout-keep-alive=30