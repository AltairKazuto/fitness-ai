@echo off
REM Start frontend in a new window
echo Starting frontend...
start "" cmd /k "cd frontend && npm run dev"

REM Start backend in a new window
echo Starting backend...
start "" cmd /k "cd backend && python backend.py"

echo Both frontend and backend are running.
pause
