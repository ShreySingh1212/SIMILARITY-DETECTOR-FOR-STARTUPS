@echo off
echo Starting Startup Similarity Detector...

echo 1. Starting Backend...
start cmd /k "cd backend && python -m venv venv && call venv\Scripts\activate && pip install -r requirements.txt && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo 2. Starting Frontend...
start cmd /k "cd frontend && npm install && npm run dev"

echo Done! Two new terminal windows should open to run the backend and frontend.
