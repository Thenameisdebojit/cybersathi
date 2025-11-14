@echo off
REM CyberSathi - One-Click Startup Script for Windows
REM This script starts both frontend and backend servers

echo ===============================================
echo    CyberSathi - Cybercrime Management System
echo    Starting Application...
echo ===============================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)

echo [INFO] Prerequisites check passed!
echo.

REM Create uploads directory
if not exist "backend\data\uploads" (
    echo [INFO] Creating uploads directory...
    mkdir backend\data\uploads
)

REM Install frontend dependencies
echo [INFO] Installing frontend dependencies...
cd frontend
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install frontend dependencies!
    pause
    exit /b 1
)
cd ..

REM Install backend dependencies
echo [INFO] Installing backend dependencies...
echo [INFO] This may take a few minutes on first run...
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to install backend dependencies!
    echo.
    echo Common fixes:
    echo 1. Make sure you have Python 3.11 or newer (not 3.13)
    echo 2. Try running: pip install --upgrade setuptools wheel
    echo 3. If pandas/numpy fails, they're optional - comment them out in requirements.txt
    echo.
    pause
    exit /b 1
)
cd ..

echo.
echo [SUCCESS] Dependencies installed!
echo.
echo ===============================================
echo    Starting Servers...
echo ===============================================
echo.
echo [INFO] Backend will run on: http://localhost:8000
echo [INFO] Frontend will run on: http://localhost:5000
echo [INFO] API Documentation: http://localhost:8000/docs
echo.
echo Default Login:
echo   Email: admin@cybersathi.in
echo   Password: Admin@1930
echo.
echo ===============================================
echo.

REM Start backend in new window
start "CyberSathi Backend" cmd /k "cd backend && python -m uvicorn app.main:app --host localhost --port 8000 --reload"

REM Wait 3 seconds for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window
start "CyberSathi Frontend" cmd /k "cd frontend && npm run dev"

echo [SUCCESS] Servers started!
echo.
echo Press any key to exit this window...
echo (The servers will continue running in separate windows)
pause >nul
