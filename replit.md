# CyberSathi - Cybercrime Helpline Assistant

## Overview
CyberSathi is an intelligent WhatsApp chatbot system designed to assist citizens in reporting cybercrimes and interfacing with India's National Cybercrime Reporting Portal (1930 Helpline).

**Current State**: Successfully imported from GitHub and configured for Replit environment. Both frontend and backend are running with proper proxy configuration.

## Project Architecture

### Frontend (React + Vite)
- **Framework**: React 18 with Vite build tool
- **Port**: 5000 (webview)
- **Features**: 
  - WhatsApp-style chat interface
  - Real-time complaint tracking dashboard
  - Admin management interface
  - Analytics charts

### Backend (FastAPI + Python)
- **Framework**: FastAPI with Uvicorn server
- **Port**: 8000 (internal, proxied through frontend)
- **Database**: SQLite (cybersathi.db)
- **Features**:
  - RESTful API for complaints, tracking, escalation
  - Database initialization on startup
  - CORS configured for frontend communication
  - JWT authentication ready
  - CyberPortal integration architecture

## Recent Changes
- **2025-11-09**: Initial Replit setup completed
  - Configured Vite to use port 5000 with proxy for backend API calls
  - Set up FastAPI backend on port 8000 with environment-based configuration
  - Fixed uvicorn logging issues for clean startup
  - Both frontend and backend workflows running successfully

## Development Workflow

### Local Development
1. **Frontend**: Runs on port 5000 with hot module replacement
2. **Backend**: Runs on port 8000, accessed via Vite proxy
3. **API Calls**: Frontend makes relative URL requests (e.g., `/api/v1/complaints/`) which Vite proxies to `http://localhost:8000`

### Key Files
- `frontend/vite.config.js` - Vite configuration with proxy setup
- `frontend/src/services/api.js` - Axios API client configuration
- `backend/server.py` - Backend server startup script
- `backend/app/main.py` - FastAPI application entry point
- `backend/app/config.py` - Environment configuration

## User Preferences
- **Development Mode**: Both workflows running simultaneously
- **Database**: Using SQLite for development (can upgrade to PostgreSQL for production)
- **Logging**: Minimal logging to avoid uvicorn formatting issues

## Tech Stack
- **Frontend**: React 18, Vite, React Router, Axios
- **Backend**: FastAPI, SQLAlchemy, Pydantic, Uvicorn
- **Database**: SQLite (development), PostgreSQL ready
- **Optional**: Rasa NLP engine, WhatsApp integration (requires API credentials)

## Integration Points

### WhatsApp API (Not Yet Configured)
- Requires Meta Cloud API or Twilio credentials
- Configure in backend/.env with WHATSAPP_API_URL and WHATSAPP_API_TOKEN

### NCRP Portal API (Mock Mode)
- Currently using mock mode
- Production requires real API credentials from cybercrime.gov.in

## API Endpoints
- `GET /health` - Health check
- `POST /api/v1/complaints/` - Register new complaint
- `GET /api/v1/tracking/{reference_id}` - Track complaint status
- `POST /api/v1/escalation/` - Escalate complaint

## Environment Variables
- `DEBUG`: Enable/disable debug mode (default: True for dev)
- `PORT`: Backend server port (default: 8000)
- `VITE_API_URL`: Frontend API URL (leave empty for proxy mode)
- `WHATSAPP_API_URL`: WhatsApp provider API base URL
- `WHATSAPP_API_TOKEN`: WhatsApp API bearer token
- `CYBERPORTAL_API_KEY`: Cybercrime portal API key

## Next Steps (Production-Grade Transformation)
1. **PROMPT 0**: Architecture audit and detailed enhancement plan
2. **PROMPT 1**: UI/UX transformation with Next.js + Tailwind + ShadCN
3. **PROMPT 2**: Backend enhancement with MongoDB/PostgreSQL and WhatsApp webhooks
4. **PROMPT 3**: NCRP Portal integration, async jobs, audit logs, admin roles

## Deployment
- **Type**: Autoscale deployment
- **Build**: Frontend build with npm
- **Run**: Backend + Frontend preview server
- **Public URL**: Available after deployment via Replit

---

**Status**: ✅ Basic import complete, ready for production-grade transformations
