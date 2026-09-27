#!/bin/bash
echo "Starting Tamil Cultural Engine..."

# Start Backend (runs from project root where main.py lives)
echo "Starting backend..."
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt > /dev/null
uvicorn main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Start Frontend
echo "Starting frontend..."
cd frontend
npm install > /dev/null
npm run dev -- --port 5173 &
FRONTEND_PID=$!

echo "Both servers are starting!"
echo "Backend is running on http://127.0.0.1:8000"
echo "Frontend is running on http://localhost:5173"
echo "Press Ctrl+C to stop both servers."

trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM
wait
