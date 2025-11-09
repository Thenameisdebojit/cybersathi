#!/usr/bin/env bash
# scripts/startup_complete.sh
# Complete startup script with all checks and fixes
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REQUIRED_DIRS=(
    "backend/app/models"
    "backend/app/services"
    "backend/app/routers"
    "backend/tests"
    "frontend/src"
    "frontend/public"
)

echo "🚀 CyberSathi Complete Startup Script"
echo "======================================"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Docker is running"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose not found. Please install docker-compose.${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} docker-compose is available"

# Create required directories
echo ""
echo "📁 Creating required directories..."
for dir in "${REQUIRED_DIRS[@]}"; do
    mkdir -p "$REPO_ROOT/$dir"
    echo -e "${GREEN}✓${NC} Created $dir"
done

# Create __init__.py files
echo ""
echo "📝 Creating __init__.py files..."
for dir in "${REQUIRED_DIRS[@]}"; do
    if [[ "$dir" == backend/* ]]; then
        touch "$REPO_ROOT/$dir/__init__.py"
        echo -e "${GREEN}✓${NC} Created $dir/__init__.py"
    fi
done

# Check if required files exist
echo ""
echo "🔍 Checking required files..."

REQUIRED_FILES=(
    "backend/requirements.txt"
    "backend/Dockerfile"
    "backend/app/main.py"
    "frontend/package.json"
    "frontend/Dockerfile"
    "frontend/index.html"
    "infra/docker-compose.yml"
)

MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$REPO_ROOT/$file" ]; then
        MISSING_FILES+=("$file")
        echo -e "${RED}✗${NC} Missing: $file"
    else
        echo -e "${GREEN}✓${NC} Found: $file"
    fi
done

if [ ${#MISSING_FILES[@]} -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Some required files are missing. Please create them first.${NC}"
    echo "   Refer to SETUP_GUIDE.md for details"
fi

# Stop any existing containers
echo ""
echo "🛑 Stopping existing containers..."
cd "$REPO_ROOT/infra"
docker-compose down -v 2>/dev/null || true
echo -e "${GREEN}✓${NC} Stopped existing containers"

# Build and start services
echo ""
echo "🏗️  Building and starting services..."
echo "   This may take several minutes on first run..."

if docker-compose up --build -d; then
    echo -e "${GREEN}✓${NC} Services started successfully"
else
    echo -e "${RED}❌ Failed to start services${NC}"
    echo "   Run 'docker-compose logs' to see error details"
    exit 1
fi

# Wait for services to be healthy
echo ""
echo "⏳ Waiting for services to become healthy..."
sleep 5

# Check backend health
MAX_RETRIES=30
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Backend is healthy"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
        echo -e "${RED}❌ Backend health check failed${NC}"
        echo "   Check logs with: docker-compose logs backend"
        exit 1
    fi
    echo -n "."
    sleep 2
done

# Check PostgreSQL
if docker exec cybersathi-postgres pg_isready -U admin > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} PostgreSQL is ready"
else
    echo -e "${YELLOW}⚠️  PostgreSQL might not be ready${NC}"
fi

# Display service URLs
echo ""
echo "======================================"
echo -e "${GREEN}✅ CyberSathi is now running!${NC}"
echo "======================================"
echo ""
echo "📍 Service URLs:"
echo "   Backend API:  http://localhost:8000"
echo "   API Docs:     http://localhost:8000/docs"
echo "   Frontend:     http://localhost:5173"
echo "   PostgreSQL:   localhost:5432"
echo ""
echo "📊 Service Status:"
docker-compose ps
echo ""
echo "📝 Useful Commands:"
echo "   View logs:        docker-compose logs -f"
echo "   Stop services:    docker-compose down"
echo "   Restart:          docker-compose restart"
echo "   Check health:     curl http://localhost:8000/health"
echo ""
echo "🧪 Test the API:"
echo "   cd $REPO_ROOT/scripts && bash demo.sh"
echo ""
echo -e "${GREEN}Setup complete! Happy coding! 🎉${NC}"