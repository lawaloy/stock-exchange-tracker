@echo off
REM Script to set up daily automatic stock data updates
REM Run this as Administrator

echo ====================================
echo Stock Tracker - Scheduled Updates Setup
echo ====================================
echo.

REM Get the current directory
set SCRIPT_DIR=%~dp0
set PYTHON_SCRIPT=%SCRIPT_DIR%main.py
set TASK_NAME=StockTrackerDailyUpdate

echo Project Directory: %SCRIPT_DIR%
echo Python Script: %PYTHON_SCRIPT%
echo.

REM Check if Python script exists
if not exist "%PYTHON_SCRIPT%" (
    echo ERROR: main.py not found at %PYTHON_SCRIPT%
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

echo Creating scheduled task...
echo Task will run daily at 4:30 PM (after market close)
echo.

REM Create the scheduled task
schtasks /create /tn "%TASK_NAME%" /tr "python \"%PYTHON_SCRIPT%\"" /sc daily /st 16:30 /f /rl HIGHEST

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ SUCCESS! Scheduled task created successfully.
    echo.
    echo Task Name: %TASK_NAME%
    echo Schedule: Daily at 4:30 PM
    echo Action: Fetch latest stock data from Finnhub API
    echo.
    echo The stock tracker will now run automatically every day!
    echo Your dashboard will always show fresh data.
    echo.
    echo To view/modify the task:
    echo - Open Task Scheduler (taskschd.msc)
    echo - Look for "%TASK_NAME%"
    echo.
    echo To delete the task:
    echo   schtasks /delete /tn "%TASK_NAME%" /f
    echo.
) else (
    echo.
    echo ❌ ERROR: Failed to create scheduled task.
    echo Please make sure you're running this script as Administrator.
    echo.
    echo Right-click this file and select "Run as administrator"
    echo.
)

pause
