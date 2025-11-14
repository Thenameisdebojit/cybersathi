@echo off
REM ================================================
REM CyberSathi - Complete Startup Script for Windows
REM ================================================

echo.
echo ================================================
echo CyberSathi - Starting Application
echo ================================================
echo.

REM Check if Node.js is installed
echo [1/6] Checking Node.js installation...
where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
echo  Node.js found!
echo.

REM Check if Python is installed
echo [2/6] Checking Python installation...
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.11 from https://www.python.org/
    pause
    exit /b 1
)
echo  Python found!
echo.

REM Install Frontend Dependencies
echo [3/6] Installing Frontend Dependencies...
cd frontend
if not exist "node_modules\" (
    echo  Running npm install...
    call npm install
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to install frontend dependencies!
        pause
        exit /b 1
    )
) else (
    echo  Frontend dependencies already installed
)
cd ..
echo.

REM Setup Backend Environment
echo [4/6] Setting up Backend Environment...
cd backend

REM Check if .env exists, if not create from example
if not exist ".env" (
    echo  Creating .env file from example...
    copy .env.example .env >nul
    echo.
    echo IMPORTANT: Please edit backend/.env and add your API keys:
    echo   - MONGODB_URL: Get free cluster from https://www.mongodb.com/cloud/atlas
    echo   - OPENAI_API_KEY: Get from https://platform.openai.com
    echo.
)

REM Install Backend Dependencies using pip
echo  Installing Python dependencies...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to install backend dependencies!
    pause
    exit /b 1
)
cd ..
echo.

REM Create data directory for uploads
if not exist "data\uploads" (
    mkdir data\uploads
    echo  Created uploads directory
)
echo.

echo [5/6] Starting Backend Server...
start "CyberSathi Backend" cmd /c "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo  Backend server starting on http://localhost:8000
echo.

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

echo [6/6] Starting Frontend Server...
start "CyberSathi Frontend" cmd /c "cd frontend && npm run dev -- --host 0.0.0.0 --port 5000"
echo  Frontend server starting on http://localhost:5000
echo.

echo.
echo ================================================
echo CyberSathi Started Successfully!
echo ================================================
echo.
echo  Frontend: http://localhost:5000
echo  Backend API: http://localhost:8000
echo  API Docs: http://localhost:8000/docs
echo.
echo  Press Ctrl+C in the server windows to stop
echo.
echo  Login credentials:
echo    Email: admin@cybersathi.in
echo    Password: Admin@1930
echo.
echo ================================================
echo.

pause
