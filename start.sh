#!/bin/bash
set -e  # Exit on any error

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt --force-reinstall --no-cache-dir

echo "Starting application on port: $PORT"
if [ -z "$PORT" ]; then
    echo "PORT environment variable not set, using default 8000"
    export PORT=8000
fi

cd backend
python -m uvicorn main:app --host=0.0.0.0 --port=$PORT