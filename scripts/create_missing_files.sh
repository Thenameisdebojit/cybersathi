#!/usr/bin/env bash
# scripts/create_missing_files.sh
# Create all missing required files for CyberSathi
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Creating missing files..."

# Create frontend/index.html
echo "Creating frontend/index.html..."
cat > "$REPO_ROOT/frontend/index.html" << 'EOF'
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CyberSathi Admin</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
EOF

# Create frontend/vite.config.js if missing
if [ ! -f "$REPO_ROOT/frontend/vite.config.js" ]; then
    echo "Creating frontend/vite.config.js..."
    cat > "$REPO_ROOT/frontend/vite.config.js" << 'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true
  },
  build: {
    outDir: 'dist',
    sourcemap: false
  }
})
EOF
fi

# Create frontend/package.json if missing
if [ ! -f "$REPO_ROOT/frontend/package.json" ]; then
    echo "Creating frontend/package.json..."
    cat > "$REPO_ROOT/frontend/package.json" << 'EOF'
{
  "name": "cybersathi-frontend",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "echo 'Linting skipped'"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.14.0",
    "axios": "^1.4.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.3",
    "vite": "^4.4.5"
  }
}
EOF
fi

# Create frontend/.eslintrc.cjs if missing
if [ ! -f "$REPO_ROOT/frontend/.eslintrc.cjs" ]; then
    echo "Creating frontend/.eslintrc.cjs..."
    cat > "$REPO_ROOT/frontend/.eslintrc.cjs" << 'EOF'
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parserOptions: { ecmaVersion: 'latest', sourceType: 'module' },
}
EOF
fi

# Create backend/pytest.ini if missing
if [ ! -f "$REPO_ROOT/backend/pytest.ini" ]; then
    echo "Creating backend/pytest.ini..."
    cat > "$REPO_ROOT/backend/pytest.ini" << 'EOF'
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
EOF
fi

# Create __init__.py files
echo "Creating __init__.py files..."
touch "$REPO_ROOT/backend/app/__init__.py"
touch "$REPO_ROOT/backend/app/models/__init__.py"
touch "$REPO_ROOT/backend/app/services/__init__.py"
touch "$REPO_ROOT/backend/app/routers/__init__.py"
touch "$REPO_ROOT/backend/tests/__init__.py"

# Create test file if missing
if [ ! -f "$REPO_ROOT/backend/tests/test_main.py" ]; then
    echo "Creating backend/tests/test_main.py..."
    cat > "$REPO_ROOT/backend/tests/test_main.py" << 'EOF'
# backend/tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_list_complaints():
    response = client.get("/api/v1/complaints/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
EOF
fi

echo ""
echo "✓ All missing files created!"
echo ""
echo "Now run: bash scripts/startup_complete.sh"