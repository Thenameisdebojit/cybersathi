@echo off
REM scripts/create_missing_files.bat
REM Create all missing required files for CyberSathi

echo Creating missing files...

SET SCRIPT_DIR=%~dp0
SET REPO_ROOT=%SCRIPT_DIR%..

REM Create frontend/index.html
echo Creating frontend/index.html...
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

REM Create frontend/vite.config.js if missing
if not exist "%REPO_ROOT%\frontend\vite.config.js" (
    echo Creating frontend/vite.config.js...
    (
    echo import { defineConfig } from 'vite'
    echo import react from '@vitejs/plugin-react'
    echo.
    echo export default defineConfig({
    echo   plugins: [react^(^)],
    echo   server: {
    echo     port: 5173,
    echo     host: true
    echo   },
    echo   build: {
    echo     outDir: 'dist',
    echo     sourcemap: false
    echo   }
    echo }^)
    ) > "%REPO_ROOT%\frontend\vite.config.js"
)

REM Create frontend/package.json if missing
if not exist "%REPO_ROOT%\frontend\package.json" (
    echo Creating frontend/package.json...
    (
    echo {
    echo   "name": "cybersathi-frontend",
    echo   "version": "0.1.0",
    echo   "type": "module",
    echo   "scripts": {
    echo     "dev": "vite",
    echo     "build": "vite build",
    echo     "preview": "vite preview",
    echo     "lint": "echo 'Linting skipped'"
    echo   },
    echo   "dependencies": {
    echo     "react": "^18.2.0",
    echo     "react-dom": "^18.2.0",
    echo     "react-router-dom": "^6.14.0",
    echo     "axios": "^1.4.0"
    echo   },
    echo   "devDependencies": {
    echo     "@vitejs/plugin-react": "^4.0.3",
    echo     "vite": "^4.4.5"
    echo   }
    echo }
    ) > "%REPO_ROOT%\frontend\package.json"
)

REM Create backend/pytest.ini if missing
if not exist "%REPO_ROOT%\backend\pytest.ini" (
    echo Creating backend/pytest.ini...
    (
    echo [pytest]
    echo testpaths = tests
    echo python_files = test_*.py
    echo python_classes = Test*
    echo python_functions = test_*
    echo addopts = -v --tb=short
    ) > "%REPO_ROOT%\backend\pytest.ini"
)

REM Create __init__.py files
echo Creating __init__.py files...
type nul > "%REPO_ROOT%\backend\app\__init__.py"
type nul > "%REPO_ROOT%\backend\app\models\__init__.py"
type nul > "%REPO_ROOT%\backend\app\services\__init__.py"
type nul > "%REPO_ROOT%\backend\app\routers\__init__.py"
type nul > "%REPO_ROOT%\backend\tests\__init__.py"

REM Create test file if missing
if not exist "%REPO_ROOT%\backend\tests\test_main.py" (
    echo Creating backend/tests/test_main.py...
    (
    echo # backend/tests/test_main.py
    echo from fastapi.testclient import TestClient
    echo from app.main import app
    echo.
    echo client = TestClient^(app^)
    echo.
    echo def test_health_endpoint^(^):
    echo     response = client.get^("/health"^)
    echo     assert response.status_code == 200
    echo     data = response.json^(^)
    echo     assert data["status"] == "ok"
    ) > "%REPO_ROOT%\backend\tests\test_main.py"
)

echo.
echo [OK] All missing files created!
echo.
echo Now run: scripts\startup_complete.bat
pause