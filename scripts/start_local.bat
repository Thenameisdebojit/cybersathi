@echo off
REM scripts\start_local.bat
REM Start CyberSathi local stack via docker-compose (Windows)

SET SCRIPT_DIR=%~dp0
SET REPO_ROOT=%SCRIPT_DIR%..
SET COMPOSE_FILE=%REPO_ROOT%\infra\docker-compose.yml

IF NOT EXIST "%COMPOSE_FILE%" (
  echo Docker compose file not found: %COMPOSE_FILE%
  pause
  exit /b 1
)

cd /d "%REPO_ROOT%\infra"
echo Building and starting services...
docker-compose -f docker-compose.yml up --build -d

echo Waiting for services to start...
timeout /t 6 /nobreak >nul

echo Services started:
echo   Backend: http://localhost:8000
echo   Rasa:    http://localhost:5005
echo   Frontend: http://localhost:5173
pause
