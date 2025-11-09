# CyberSathi - Quick Reference Guide

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd CyberSathi

# Start everything (Linux/Mac)
bash scripts/startup_complete.sh

# Start everything (Windows)
scripts\startup_complete.bat

# Verify installation
bash scripts/verify_installation.sh
```

## 📋 Essential Commands

### Docker Management
```bash
# Start services
cd infra && docker-compose up -d

# Stop services
docker-compose down

# Stop and remove everything
docker-compose down -v

# Rebuild everything
docker-compose up --build -d

# View logs
docker-compose logs -f
docker-compose logs -f backend
```

### Service Access
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:5173
- **PostgreSQL**: localhost:5432 (user: admin, pass: admin123)

### Health Checks
```bash
# Check backend
curl http://localhost:8000/health

# Check services
docker-compose ps

# Check logs
docker-compose logs backend --tail=50
```

## 🔧 Development

### Backend Development
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run locally (without Docker)
python -m app.main

# Run tests
pytest

# Initialize database
python ../scripts/db_migrate.py
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev

# Build
npm run build

# Lint
npm run lint
```

## 🐛 Common Fixes

### Reset Everything
```bash
cd infra
docker-compose down -v
docker system prune -a
docker-compose up --build -d
```

### Port Conflicts
```bash
# Find process using port
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows
```

### Database Issues
```bash
# Recreate database
docker-compose down -v
docker-compose up -d postgres
docker-compose up -d backend

# Access database
docker exec -it cybersathi-postgres psql -U admin -d cybersathi
```

### Backend Not Starting
```bash
# Check logs
docker-compose logs backend

# Restart
docker-compose restart backend

# Rebuild
docker-compose up -d --build backend
```

## 📡 API Quick Reference

### Register Complaint
```bash
curl -X POST http://localhost:8000/api/v1/complaints/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone": "+919999999999",
    "incident_type": "upi_scam",
    "description": "Lost money via UPI",
    "amount": 5000
  }'
```

### List Complaints
```bash
curl http://localhost:8000/api/v1/complaints/list
```

### Track Complaint
```bash
curl http://localhost:8000/api/v1/tracking/{reference_id}
```

### Get Specific Complaint
```bash
curl http://localhost:8000/api/v1/complaints/{reference_id}
```

## 🗄️ Database Commands

### Access PostgreSQL
```bash
docker exec -it cybersathi-postgres psql -U admin -d cybersathi
```

### Common Queries
```sql
-- List all tables
\dt

-- View complaints
SELECT * FROM complaints ORDER BY created_at DESC LIMIT 10;

-- Count complaints
SELECT COUNT(*) FROM complaints;

-- Filter by type
SELECT * FROM complaints WHERE incident_type = 'upi_scam';

-- Exit
\q
```

## 📝 File Locations

### Configuration
- Backend config: `backend/app/config.py`
- Docker compose: `infra/docker-compose.yml`
- Frontend config: `frontend/vite.config.js`
- Environment: `backend/.env`

### Source Code
- Backend API: `backend/app/`
- Frontend: `frontend/src/`
- Rasa: `backend/rasa/`

### Scripts
- Startup: `scripts/startup_complete.sh`
- Database: `scripts/db_migrate.py`
- Demo: `scripts/demo.sh`

## 🔍 Debugging

### View Container Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Access Container Shell
```bash
# Backend
docker exec -it cybersathi-backend bash

# Database
docker exec -it cybersathi-postgres psql -U admin -d cybersathi

# Frontend
docker exec -it cybersathi-frontend sh
```

### Check Container Resources
```bash
# Resource usage
docker stats

# Inspect container
docker inspect cybersathi-backend
```

## ⚙️ Environment Variables

Create `backend/.env`:
```env
DATABASE_URL=postgresql+psycopg2://admin:admin123@localhost:5432/cybersathi
JWT_SECRET=your-secret-key
DEBUG=true
FRONTEND_URL=http://localhost:5173
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest -v
pytest --cov=app
```

### API Testing
```bash
# Use the demo script
bash scripts/demo.sh

# Or use curl
curl -X POST http://localhost:8000/api/v1/complaints/ \
  -H "Content-Type: application/json" \
  -d @test_data.json
```

## 📊 Monitoring

### Check Service Status
```bash
docker-compose ps
```

### Check Health
```bash
curl http://localhost:8000/health
```

### View Metrics
```bash
docker stats cybersathi-backend
```

## 🔐 Security Notes

- Change default passwords in production
- Update `JWT_SECRET` in `.env`
- Use HTTPS in production
- Enable authentication for API endpoints
- Secure PostgreSQL access

## 📚 Additional Resources

- Full setup guide: `SETUP_GUIDE.md`
- Troubleshooting: `TROUBLESHOOTING.md`
- API documentation: http://localhost:8000/docs
- Architecture docs: `docs/architecture.md`

## 💡 Tips

1. Always check logs first: `docker-compose logs -f`
2. Use health endpoints to verify services
3. Keep Docker Desktop updated
4. Allocate enough resources (4GB RAM minimum)
5. Run verify script after setup: `bash scripts/verify_installation.sh`