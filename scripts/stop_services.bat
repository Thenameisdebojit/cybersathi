@echo off
REM scripts\stop_services.bat
REM Stop CyberSathi docker-compose stack (Windows)

SET SCRIPT_DIR=%~dp0
SET REPO_ROOT=%SCRIPT_DIR%..
SET COMPOSE_FILE=%REPO_ROOT%\infra\docker-compose.yml

IF NOT EXIST "%COMPOSE_FILE%" (
  echo docker-compose.yml not found: %COMPOSE_FILE%
  pause
  exit /b 1
)

cd /d "%REPO_ROOT%\infra"
echo Stopping docker-compose stack...
docker-compose -f docker-compose.yml down --volumes --remove-orphans
echo Stopped.
pause
