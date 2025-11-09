#!/usr/bin/env bash
# scripts/verify_installation.sh
# Verify CyberSathi installation and configuration
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASS_COUNT++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAIL_COUNT++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARN_COUNT++))
}

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}CyberSathi Installation Verification${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""

# 1. Check system requirements
echo -e "${BLUE}[1/8]${NC} Checking system requirements..."

if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
    check_pass "Docker installed (version $DOCKER_VERSION)"
else
    check_fail "Docker not installed"
fi

if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f3 | cut -d',' -f1)
    check_pass "docker-compose installed (version $COMPOSE_VERSION)"
else
    check_fail "docker-compose not installed"
fi

if docker info &> /dev/null; then
    check_pass "Docker daemon is running"
else
    check_fail "Docker daemon is not running"
fi

echo ""

# 2. Check directory structure
echo -e "${BLUE}[2/8]${NC} Checking directory structure..."

REQUIRED_DIRS=(
    "backend/app"
    "backend/app/models"
    "backend/app/services"
    "backend/app/routers"
    "backend/rasa"
    "backend/tests"
    "frontend/src"
    "frontend/public"
    "infra"
    "scripts"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$REPO_ROOT/$dir" ]; then
        check_pass "Directory exists: $dir"
    else
        check_fail "Missing directory: $dir"
    fi
done

echo ""

# 3. Check required files
echo -e "${BLUE}[3/8]${NC} Checking required files..."

REQUIRED_FILES=(
    "backend/Dockerfile"
    "backend/requirements.txt"
    "backend/app/main.py"
    "backend/app/config.py"
    "backend/app/__init__.py"
    "frontend/Dockerfile"
    "frontend/package.json"
    "frontend/index.html"
    "frontend/vite.config.js"
    "infra/docker-compose.yml"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$REPO_ROOT/$file" ]; then
        check_pass "File exists: $file"
    else
        check_fail "Missing file: $file"
    fi
done

echo ""

# 4. Check Python __init__.py files
echo -e "${BLUE}[4/8]${NC} Checking Python package initialization..."

INIT_FILES=(
    "backend/app/__init__.py"
    "backend/app/models/__init__.py"
    "backend/app/services/__init__.py"
    "backend/app/routers/__init__.py"
    "backend/tests/__init__.py"
)

for file in "${INIT_FILES[@]}"; do
    if [ -f "$REPO_ROOT/$file" ]; then
        check_pass "Init file exists: $file"
    else
        check_warn "Missing init file: $file (will be created on startup)"
    fi
done

echo ""

# 5. Check Docker containers
echo -e "${BLUE}[5/8]${NC} Checking Docker containers..."

cd "$REPO_ROOT/infra"

if docker-compose ps | grep -q "Up"; then
    check_pass "Docker containers are running"
    
    # Check individual services
    if docker-compose ps postgres | grep -q "Up"; then
        check_pass "PostgreSQL container is up"
    else
        check_warn "PostgreSQL container is not running"
    fi
    
    if docker-compose ps backend | grep -q "Up"; then
        check_pass "Backend container is up"
    else
        check_warn "Backend container is not running"
    fi
    
    if docker-compose ps frontend | grep -q "Up"; then
        check_pass "Frontend container is up"
    else
        check_warn "Frontend container is not running"
    fi
else
    check_warn "No containers are running (run startup script to start)"
fi

echo ""

# 6. Check ports
echo -e "${BLUE}[6/8]${NC} Checking port availability..."

check_port() {
    local port=$1
    local service=$2
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        check_pass "Port $port is in use ($service)"
    else
        check_warn "Port $port is not in use ($service not running?)"
    fi
}

check_port 8000 "Backend"
check_port 5173 "Frontend"
check_port 5432 "PostgreSQL"

echo ""

# 7. Check API endpoints
echo -e "${BLUE}[7/8]${NC} Checking API endpoints..."

if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    check_pass "Backend health endpoint responding"
    
    HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
    if echo "$HEALTH_RESPONSE" | grep -q "ok"; then
        check_pass "Backend health check returns OK"
    else
        check_warn "Backend health check response unexpected"
    fi
else
    check_warn "Backend health endpoint not responding (is backend running?)"
fi

if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    check_pass "API documentation accessible"
else
    check_warn "API documentation not accessible"
fi

if curl -s http://localhost:5173 > /dev/null 2>&1; then
    check_pass "Frontend accessible"
else
    check_warn "Frontend not accessible (is frontend running?)"
fi

echo ""

# 8. Check database
echo -e "${BLUE}[8/8]${NC} Checking database..."

if docker exec cybersathi-postgres pg_isready -U admin > /dev/null 2>&1; then
    check_pass "PostgreSQL is ready"
    
    # Check if tables exist
    TABLE_COUNT=$(docker exec cybersathi-postgres psql -U admin -d cybersathi -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ')
    
    if [ "$TABLE_COUNT" -gt 0 ]; then
        check_pass "Database tables exist (count: $TABLE_COUNT)"
    else
        check_warn "No database tables found (run db_migrate.py)"
    fi
else
    check_warn "PostgreSQL not ready or not running"
fi

echo ""

# Summary
echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}Verification Summary${NC}"
echo -e "${BLUE}=====================================${NC}"
echo -e "${GREEN}Passed:${NC} $PASS_COUNT"
echo -e "${YELLOW}Warnings:${NC} $WARN_COUNT"
echo -e "${RED}Failed:${NC} $FAIL_COUNT"
echo ""

if [ $FAIL_COUNT -eq 0 ] && [ $WARN_COUNT -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! CyberSathi is properly configured.${NC}"
    exit 0
elif [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Installation complete with warnings.${NC}"
    echo "Some services might not be running. Run startup script if needed."
    exit 0
else
    echo -e "${RED}❌ Installation has issues that need to be fixed.${NC}"
    echo "Please review the failed checks above."
    exit 1
fi