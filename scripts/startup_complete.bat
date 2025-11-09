@echo off
REM scripts/startup_complete.bat
REM Complete startup script for Windows
setlocal enabledelayedexpansion

echo ========================================
echo CyberSathi Complete Startup Script
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo [OK] Docker is running

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] docker-compose not found. Please install docker-compose.
    pause
    exit /b 1
)
echo [OK] docker-compose is available

REM Get script directory
set SCRIPT_DIR=%~dp0
set REPO_ROOT=%SCRIPT_DIR%..

echo.
echo Creating required directories...
mkdir "%REPO_ROOT%\backend\app\models" 2>nul
mkdir "%REPO_ROOT%\backend\app\services" 2>nul
mkdir "%REPO_ROOT%\backend\app\routers" 2>nul
mkdir "%REPO_ROOT%\backend\tests" 2>nul
mkdir "%REPO_ROOT%\frontend\src" 2>nul
mkdir "%REPO_ROOT%\frontend\public" 2>nul
echo [OK] Directories created

echo.
echo Creating required files...
REM Create frontend/index.html
if not exist "%REPO_ROOT%\frontend\index.html" (
    (
    echo ^<!doctype html^>
    echo ^<html lang="en"^>
    echo   ^<head^>
    echo     ^<meta charset="utf-8" /^>
    echo     ^<meta name="viewport" content="width=device-width, initial-scale=1.0" /^>
    echo     ^<title^>CyberSathi Admin^</title^>
    echo   ^</head^>
    echo   ^<body^>
    echo     ^<div id="root"^>^</div^>
    echo     ^<script type="module" src="/src/main.jsx"^>^</script^>
    echo   ^</body^>
    echo ^</html^>
    ) > "%REPO_ROOT%\frontend\index.html"
)
REM Create __init__.py files
type nul > "%REPO_ROOT%\backend\app\__init__.py"
type nul > "%REPO_ROOT%\backend\app\models\__init__.py"
type nul > "%REPO_ROOT%\backend\app\services\__init__.py"
type nul > "%REPO_ROOT%\backend\app\routers\__init__.py"
type nul > "%REPO_ROOT%\backend\tests\__init__.py"
echo [OK] Required files created

REM Stop existing containers
echo.
echo Stopping existing containers...
cd /d "%REPO_ROOT%\infra"
docker-compose down -v 2>nul
echo [OK] Stopped existing containers

REM Build and start services
echo.
echo Building and starting services...
echo This may take several minutes on first run...
docker-compose up --build -d
if errorlevel 1 (
    echo [ERROR] Failed to start services
    echo Run 'docker-compose logs' to see error details
    pause
    exit /b 1
)
echo [OK] Services started successfully

REM Wait for services
echo.
echo Waiting for services to become healthy...
timeout /t 10 /nobreak >nul

REM Check backend health
echo Checking backend health...
set MAX_RETRIES=30
set RETRY_COUNT=0

:health_check_loop
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Backend is healthy
    goto health_check_done
)
set /a RETRY_COUNT+=1
if %RETRY_COUNT% geq %MAX_RETRIES% (
    echo [ERROR] Backend health check failed
    echo Check logs with: docker-compose logs backend
    pause
    exit /b 1
)
echo|set /p="."
timeout /t 2 /nobreak >nul
goto health_check_loop

:health_check_done

REM Display results
echo.
echo ========================================
echo CyberSathi is now running!
echo ========================================
echo.
echo Service URLs:
echo   Backend API:  http://localhost:8000
echo   API Docs:     http://localhost:8000/docs
echo   Frontend:     http://localhost:5173
echo   PostgreSQL:   localhost:5432
echo.
echo Service Status:
docker-compose ps
echo.
echo Useful Commands:
echo   View logs:        docker-compose logs -f
echo   Stop services:    docker-compose down
echo   Restart:          docker-compose restart
echo   Check health:     curl http://localhost:8000/health
echo.
echo Test the API:
echo   cd %REPO_ROOT%\scripts ^&^& demo.bat
echo.
echo Setup complete! Happy coding!
echo.
pause