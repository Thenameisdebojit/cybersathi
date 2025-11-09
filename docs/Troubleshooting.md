# CyberSathi Troubleshooting Guide

## 🔧 Common Issues and Solutions

### 1. Docker Issues

#### Docker not running
```bash
# Error: Cannot connect to Docker daemon
# Solution: Start Docker Desktop or Docker service

# Linux
sudo systemctl start docker

# macOS/Windows
# Start Docker Desktop application
```

#### Port already in use
```bash
# Error: Bind for 0.0.0.0:8000 failed: port is already allocated

# Find what's using the port
# Linux/Mac
lsof -i :8000
sudo lsof -i :8000

# Windows
netstat -ano | findstr :8000

# Kill the process or change the port in docker-compose.yml
```

#### Permission denied
```bash
# Error: permission denied while trying to connect to Docker daemon

# Linux - Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Then restart Docker
sudo systemctl restart docker
```

### 2. Database Issues

#### Database connection failed
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres

# If persistent, recreate database
docker-compose down -v
docker-compose up -d
```

#### Database not initialized
```bash
# Run migration script
cd backend
python ../scripts/db_migrate.py

# Or manually initialize inside container
docker exec -it cybersathi-backend python -c "from app.services.db_service import init_db; init_db()"
```

#### Can't connect to PostgreSQL from host
```bash
# Ensure port 5432 is exposed in docker-compose.yml
# Try connecting
docker exec -it cybersathi-postgres psql -U admin -d cybersathi

# If successful, check password and connection string
```

### 3. Backend Issues

#### ModuleNotFoundError
```bash
# Error: No module named 'app'

# Solution 1: Check PYTHONPATH
export PYTHONPATH=/app  # Inside container
export PYTHONPATH=$(pwd)  # Local dev

# Solution 2: Reinstall dependencies
cd backend
pip install -r requirements.txt

# Solution 3: Rebuild container
docker-compose build backend
docker-compose up -d backend
```

#### Import errors in routers
```bash
# Ensure all __init__.py files exist
touch backend/app/__init__.py
touch backend/app/models/__init__.py
touch backend/app/services/__init__.py
touch backend/app/routers/__init__.py
```

#### Backend not responding
```bash
# Check backend logs
docker-compose logs backend

# Check health endpoint
curl http://localhost:8000/health

# Restart backend
docker-compose restart backend

# Check if port 8000 is accessible
telnet localhost 8000
```

#### Pydantic validation errors
```bash
# Error: validation error for Settings

# Check .env file exists and has correct format
cd backend
cp ../.env.example .env
# Edit .env with your values

# Verify no typos in environment variable names
```

### 4. Frontend Issues

#### npm install fails
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### Build fails
```bash
# Check for syntax errors
npm run lint

# Try building locally first
npm run build

# Check vite.config.js exists
# Check all imports are correct
```

#### Frontend not loading
```bash
# Check if container is running
docker-compose ps frontend

# Check frontend logs
docker-compose logs frontend

# Verify nginx configuration
docker exec -it cybersathi-frontend cat /etc/nginx/conf.d/default.conf

# Try accessing directly
curl http://localhost:5173
```

#### CORS errors
```bash
# Check backend CORS settings in app/main.py
# Ensure FRONTEND_URL matches your frontend URL

# For development, set DEBUG=true in backend/.env
DEBUG=true

# Restart backend after changes
docker-compose restart backend
```

### 5. API Issues

#### 404 Not Found
```bash
# Verify endpoint exists
curl http://localhost:8000/docs

# Check router is included in main.py
# Verify URL path matches router definition
```

#### 500 Internal Server Error
```bash
# Check backend logs for stack trace
docker-compose logs backend | tail -50

# Common causes:
# - Database not initialized
# - Missing environment variables
# - Code syntax errors
```

#### Request timeout
```bash
# Check if backend is responding
curl -v http://localhost:8000/health

# Increase timeout in frontend
# Edit frontend/src/services/api.js
# Change timeout value
```

### 6. Docker Compose Issues

#### Services won't start
```bash
# Check docker-compose.yml syntax
docker-compose config

# View all logs
docker-compose logs

# Start services one by one
docker-compose up postgres
docker-compose up backend
docker-compose up frontend
```

#### Build errors
```bash
# Clean build
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# Remove all unused Docker resources
docker system prune -a
```

#### Container keeps restarting
```bash
# Check why container is restarting
docker-compose logs --tail=100 <service-name>

# Check health check configuration
docker inspect cybersathi-backend | grep -A 10 Health

# Disable restart policy temporarily
# Edit docker-compose.yml, change restart: unless-stopped to restart: "no"
```

### 7. Network Issues

#### Can't access services from host
```bash
# Check if ports are mapped correctly
docker-compose ps

# Check if services are listening
docker exec cybersathi-backend netstat -tuln | grep 8000

# Check firewall settings
# Linux
sudo ufw status
sudo ufw allow 8000

# Windows - check Windows Firewall settings
```

#### Services can't communicate
```bash
# Check if services are on same network
docker network ls
docker network inspect infra_default

# Verify service names in docker-compose.yml
# Use service names as hostnames (e.g., postgres:5432)
```

### 8. Performance Issues

#### Slow startup
```bash
# Normal on first run due to image downloads and builds
# Subsequent starts should be faster

# Check system resources
docker stats

# Increase Docker resources in Docker Desktop settings
# Recommended: 4GB RAM, 2 CPUs minimum
```

#### High CPU usage
```bash
# Check which container is using resources
docker stats

# Check for infinite loops in code
# Review backend logs for repeated errors
```

## 🔍 Debugging Commands

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Check service status
```bash
# List all containers
docker-compose ps

# Inspect container
docker inspect cybersathi-backend

# Check health
curl http://localhost:8000/health
```

### Access container shell
```bash
# Backend
docker exec -it cybersathi-backend bash
# or
docker exec -it cybersathi-backend sh

# PostgreSQL
docker exec -it cybersathi-postgres psql -U admin -d cybersathi

# Frontend
docker exec -it cybersathi-frontend sh
```

### Database queries
```bash
# Connect to database
docker exec -it cybersathi-postgres psql -U admin -d cybersathi

# List tables
\dt

# View complaints
SELECT * FROM complaints LIMIT 10;

# Count records
SELECT COUNT(*) FROM complaints;

# Exit
\q
```

### Check file structure
```bash
# Backend
docker exec cybersathi-backend ls -la /app
docker exec cybersathi-backend ls -la /app/app

# Frontend
docker exec cybersathi-frontend ls -la /usr/share/nginx/html
```

## 🧪 Testing

### Test backend endpoints
```bash
# Health check
curl http://localhost:8000/health

# List complaints
curl http://localhost:8000/api/v1/complaints/list

# Create complaint
curl -X POST http://localhost:8000/api/v1/complaints/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+919999999999",
    "incident_type": "test",
    "description": "test complaint"
  }'
```

### Run unit tests
```bash
# Inside backend container
docker exec cybersathi-backend pytest

# Or locally
cd backend
pytest
```

## 📝 Log Files

### Backend logs
```bash
# Application logs
docker-compose logs backend

# Uvicorn access logs
docker-compose logs backend | grep "GET\|POST\|PUT\|DELETE"
```

### PostgreSQL logs
```bash
docker-compose logs postgres
```

### Nginx logs (Frontend)
```bash
docker exec cybersathi-frontend cat /var/log/nginx/access.log
docker exec cybersathi-frontend cat /var/log/nginx/error.log
```

## 🔄 Reset Everything

If nothing else works, complete reset:

```bash
# Stop all services
docker-compose down -v

# Remove all containers, images, networks
docker system prune -a --volumes

# Remove any SQLite database files
rm backend/*.db

# Start fresh
docker-compose up --build -d
```

## 📞 Getting Help

If issues persist:

1. Check all error messages carefully
2. Review logs: `docker-compose logs -f`
3. Verify all required files exist
4. Check environment variables
5. Ensure Docker has enough resources
6. Try the complete reset procedure above

## ✅ Health Check Checklist

- [ ] Docker is running
- [ ] All ports are free (8000, 5173, 5432)
- [ ] All required files exist
- [ ] Environment variables are set
- [ ] Database is initialized
- [ ] Backend health check passes
- [ ] Frontend loads in browser
- [ ] API endpoints respond