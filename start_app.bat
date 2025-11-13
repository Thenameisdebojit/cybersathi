@echo off
REM CyberSathi Application Startup Script for Windows
REM This script starts MongoDB, Backend, and Frontend services

echo =========================================
echo    Starting CyberSathi Application
echo =========================================
echo.

REM Check if MongoDB is installed
where mongod >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] MongoDB is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if npm is installed
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js/npm is not installed or not in PATH
    pause
    exit /b 1
)

echo [OK] All requirements satisfied
echo.

REM Create data directory for MongoDB
echo Setting up MongoDB data directory...
if not exist "data\db" mkdir data\db
echo [OK] Data directory ready
echo.

REM Start MongoDB
echo Starting MongoDB...
start "MongoDB" mongod --dbpath ./data/db --bind_ip 127.0.0.1 --noauth
timeout /t 3 /nobreak >nul
echo [OK] MongoDB started
echo.

REM Start Backend
echo Starting Backend API...
cd backend
start "CyberSathi Backend" python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
cd ..
timeout /t 3 /nobreak >nul
echo [OK] Backend started
echo   - API running at: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo.

REM Start Frontend
echo Starting Frontend...
cd frontend
start "CyberSathi Frontend" npm run dev
cd ..
timeout /t 3 /nobreak >nul
echo [OK] Frontend started
echo   - App running at: http://localhost:5000
echo.

echo =========================================
echo    CyberSathi is now running!
echo =========================================
echo.
echo Services:
echo   * MongoDB:  Running on port 27017
echo   * Backend:  http://localhost:8000
echo   * Frontend: http://localhost:5000
echo.
echo Admin Credentials (Default):
echo   Email:    admin@cybersathi.in
echo   Password: Admin@1930
echo.
echo Close all command windows to stop services
echo.
pause
