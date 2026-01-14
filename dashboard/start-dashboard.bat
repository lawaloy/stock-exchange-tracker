@echo off
REM Windows batch script to start both backend and frontend

echo Starting Stock Exchange Tracker Dashboard...
echo.

REM Start backend in a new window
echo Starting backend server...
start "Dashboard Backend" cmd /k "cd backend && python main.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend in a new window
echo Starting frontend...
start "Dashboard Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Dashboard is starting!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to stop both servers...
pause > nul

REM Close the started windows
taskkill /FI "WindowTitle eq Dashboard Backend*" /T /F
taskkill /FI "WindowTitle eq Dashboard Frontend*" /T /F
