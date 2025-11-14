#!/bin/bash

# CyberSathi Application Startup Script (Replit Environment)
# This script starts Backend and Frontend services

echo "========================================="
echo "   Starting CyberSathi Application      "
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if required commands exist
echo -e "${BLUE}Checking system requirements...${NC}"

if ! command_exists python && ! command_exists python3; then
    echo -e "${RED}✗ Python is not installed${NC}"
    exit 1
fi

if ! command_exists npm; then
    echo -e "${RED}✗ Node.js/npm is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All requirements satisfied${NC}"
echo ""

# Check for .env file
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠ No .env file found in backend directory${NC}"
    echo -e "${YELLOW}ℹ Please create backend/.env from .env.example${NC}"
    echo -e "${YELLOW}ℹ Make sure to configure MONGODB_URL with your MongoDB Atlas connection string${NC}"
    echo ""
fi

# Use python3 if python is not available
PYTHON_CMD="python"
if ! command_exists python; then
    PYTHON_CMD="python3"
fi

# Start Backend (FastAPI)
echo -e "${BLUE}Starting Backend API...${NC}"
cd backend
$PYTHON_CMD -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /dev/null 2>&1 &
BACKEND_PID=$!
cd ..
sleep 3
if ps -p $BACKEND_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend started successfully (PID: $BACKEND_PID)${NC}"
    echo -e "${YELLOW}  → API running at: http://localhost:8000${NC}"
    echo -e "${YELLOW}  → API Docs: http://localhost:8000/docs${NC}"
else
    echo -e "${RED}✗ Failed to start Backend${NC}"
    exit 1
fi
echo ""

# Start Frontend (React + Vite)
echo -e "${BLUE}Starting Frontend...${NC}"
cd frontend
npm run dev > /dev/null 2>&1 &
FRONTEND_PID=$!
cd ..
sleep 3
if ps -p $FRONTEND_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Frontend started successfully (PID: $FRONTEND_PID)${NC}"
    echo -e "${YELLOW}  → App running at: http://localhost:5000${NC}"
else
    echo -e "${RED}✗ Failed to start Frontend${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi
echo ""

echo "========================================="
echo -e "${GREEN}   CyberSathi is now running!           ${NC}"
echo "========================================="
echo ""
echo "Services:"
echo "  • Backend:  http://localhost:8000"
echo "  • Frontend: http://localhost:5000"
echo ""
echo "Process IDs:"
echo "  • Backend:  $BACKEND_PID"
echo "  • Frontend: $FRONTEND_PID"
echo ""
echo "Admin Credentials (Default):"
echo "  Email:    admin@cybersathi.in"
echo "  Password: Check ADMIN_PASSWORD in your .env file"
echo ""
echo -e "${YELLOW}IMPORTANT:${NC}"
echo "  - Make sure MongoDB Atlas is configured in backend/.env"
echo "  - MONGODB_URL should point to your cloud database"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Trap Ctrl+C to clean up
trap "echo ''; echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'All services stopped.'; exit 0" INT

# Wait for all processes
wait
