#!/bin/bash

# Startup script for FastAPI server

echo "Starting Startup Analysis API Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt  # All requirements are now in one file

# Run the API server
echo "Starting FastAPI server on http://localhost:8000"
echo "API Documentation available at http://localhost:8000/docs"
echo "Press Ctrl+C to stop the server"

# Run with hot reload for development
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
