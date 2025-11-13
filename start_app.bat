@echo off
REM CyberSathi Application Startup Script for Windows (Replit Environment)
REM This script starts Backend and Frontend services

echo =========================================
echo    Starting CyberSathi Application
echo =========================================
echo.

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

REM Check for .env file
if not exist "backend\.env" (
    echo [WARNING] No .env file found in backend directory
    echo [INFO] Please create backend\.env from .env.example
    echo [INFO] Make sure to configure MONGODB_URL with your MongoDB Atlas connection string
    pause
)

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
echo   * Backend:  http://localhost:8000
echo   * Frontend: http://localhost:5000
echo.
echo Admin Credentials (Default):
echo   Email:    admin@cybersathi.in
echo   Password: Check ADMIN_PASSWORD in your .env file
echo.
echo IMPORTANT:
echo   - Make sure MongoDB Atlas is configured in backend\.env
echo   - MONGODB_URL should point to your cloud database
echo.
echo Close all command windows to stop services
echo.
pause
