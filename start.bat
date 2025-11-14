@echo off
echo ================================================
echo   CyberSathi - Starting Application
echo ================================================
echo.

echo [1/4] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
echo     Node.js found!

echo.
echo [2/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)
echo     Python found!

echo.
echo [3/4] Installing Frontend Dependencies...
cd frontend
if not exist node_modules (
    echo     Running npm install...
    call npm install
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install frontend dependencies!
        pause
        exit /b 1
    )
) else (
    echo     Dependencies already installed (node_modules exists)
)
cd ..

echo.
echo [4/4] Installing Backend Dependencies...
cd backend
if not exist venv (
    echo     Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
)
echo     Activating virtual environment...
call venv\Scripts\activate.bat
echo     Installing Python packages...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Failed to install backend dependencies!
    pause
    exit /b 1
)
cd ..

echo.
echo ================================================
echo   Starting Backend and Frontend Servers...
echo ================================================
echo.
echo Backend API will run on: http://localhost:8000
echo Frontend UI will run on: http://localhost:5000
echo.
echo Press Ctrl+C to stop both servers
echo.

REM Start backend in new window
start "CyberSathi Backend" cmd /k "cd backend && venv\Scripts\activate && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait 3 seconds for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window
start "CyberSathi Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ================================================
echo   Both servers started successfully!
echo ================================================
echo.
echo Backend API: http://localhost:8000/docs
echo Frontend UI: http://localhost:5000
echo.
echo NOTE: If you get MongoDB connection errors, please follow MONGODB_SETUP.md
echo       to set up your FREE MongoDB Atlas database.
echo.
pause
