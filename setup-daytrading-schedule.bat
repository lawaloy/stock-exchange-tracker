@echo off
REM Day Trading Schedule Setup - 4 Updates During Market Hours (Mon-Fri only)
REM Run this as Administrator

echo ====================================
echo Stock Tracker - Day Trading Schedule
echo ====================================
echo.

set SCRIPT_DIR=%~dp0
set PYTHON_SCRIPT=%SCRIPT_DIR%main.py
set TASK_PREFIX=StockTracker_DayTrading

echo Project Directory: %SCRIPT_DIR%
echo Python Script: %PYTHON_SCRIPT%
echo.

REM Check if Python script exists
if not exist "%PYTHON_SCRIPT%" (
    echo ERROR: main.py not found
    pause
    exit /b 1
)

echo Creating 3 scheduled tasks for weekdays only...
echo.

REM Market Open - 9:00 AM
echo [1/3] Creating 9:00 AM task (Market Open)...
schtasks /create /tn "%TASK_PREFIX%_0900" /tr "python \"%PYTHON_SCRIPT%\" --top-n 50" /sc weekly /d MON,TUE,WED,THU,FRI /st 09:00 /f /rl HIGHEST

REM Midday - 12:00 PM
echo [2/3] Creating 12:00 PM task (Midday)...
schtasks /create /tn "%TASK_PREFIX%_1200" /tr "python \"%PYTHON_SCRIPT%\" --top-n 50" /sc weekly /d MON,TUE,WED,THU,FRI /st 12:00 /f /rl HIGHEST

REM Pre-Close - 3:00 PM
echo [3/3] Creating 3:00 PM task (Pre-Close)...
schtasks /create /tn "%TASK_PREFIX%_1500" /tr "python \"%PYTHON_SCRIPT%\" --top-n 50" /sc weekly /d MON,TUE,WED,THU,FRI /st 15:00 /f /rl HIGHEST

echo.
echo ✅ SUCCESS! All 3 scheduled tasks created!
echo.
echo Schedule Summary:
echo ├── 9:00 AM  - Market Open (top 50 stocks)
echo ├── 12:00 PM - Midday Update
echo └── 3:00 PM  - Pre-Close Update
echo.
echo Days: Monday - Friday only (market days)
echo API Usage: 3 updates × 60 calls = 180 calls/day ✅
echo.
echo Your dashboard will auto-update throughout the trading day!
echo.
echo To view tasks:
echo   Task Scheduler ^> Task Scheduler Library
echo   Look for "%TASK_PREFIX%_*"
echo.
echo To delete all tasks:
echo   schtasks /delete /tn "%TASK_PREFIX%_0900" /f
echo   schtasks /delete /tn "%TASK_PREFIX%_1200" /f
echo   schtasks /delete /tn "%TASK_PREFIX%_1500" /f
echo.
pause
