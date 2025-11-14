# CyberSathi - Cybercrime Complaint Management System

## Overview

CyberSathi is India's cybercrime complaint management platform designed for government agencies and law enforcement. The system enables citizens to report cybercrimes via WhatsApp chatbot integration and provides an administrative dashboard for tracking and managing complaints. It integrates with India's National Cybercrime Reporting Portal (NCRP) at cybercrime.gov.in.

**Core Purpose**: Streamline cybercrime reporting and case management with multi-language support (English, Odia), WhatsApp-based complaint collection, and automated case tracking.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture

**Framework**: FastAPI (Python 3.11+) with async/await for high-performance API operations

**Key Design Decisions**:
- **MongoDB Atlas** as primary database using Beanie ODM for async document operations
- **Motor** async driver for MongoDB connectivity with connection pooling (10-100 connections)
- **JWT-based authentication** using `python-jose` and `passlib[bcrypt]` for password hashing
- **Role-Based Access Control (RBAC)** with 5 user roles: Super Admin, Admin, Officer, Viewer, API User
- **Stateful conversation management** for WhatsApp chatbot flow tracking
- **Rule-based NLU** (no ML/LLM) using regex patterns for intent detection and entity extraction
- **Audit logging** for all system actions with MongoDB document tracking

**Security Features**:
- End-to-end encryption using Fernet (AES-256) for sensitive PII data
- PII masking for logging and display (phone, email, Aadhaar)
- Field-level encryption for specific sensitive fields
- Environment-based configuration with `.env` file separation

**Background Processing**:
- Celery with Redis backend for async task queue
- APScheduler for scheduled jobs
- Redis caching layer for performance optimization

### Frontend Architecture

**Framework**: React 18 with Vite as build tool

**Key Design Decisions**:
- **React Router DOM** for client-side routing
- **Axios** for API communication with interceptors
- **TailwindCSS** for utility-first styling with custom design system
- **Recharts** for data visualization and analytics dashboards
- **Lucide React** for icon system
- **Local storage** for authentication token persistence

**UI/UX Patterns**:
- Consistent blue gradient theme across login/signup pages
- Responsive design with mobile-first approach
- Glass morphism effects for modern UI aesthetics
- Role-based component rendering

### WhatsApp Integration

**Provider**: Meta Cloud API (WhatsApp Business API)

**Conversation Flow**:
1. **NLU-based intent detection** using keyword/regex matching (no ML required)
2. **State machine** for multi-step complaint collection with field validation
3. **13-field data collection**: Name, Phone, Email, Guardian Name, DOB, Gender, Village, Post Office, Police Station, District, PIN, Incident Details, Amount
4. **Bilingual support** (English/Odia) with i18n JSON translation files
5. **Webhook verification** using HMAC signature validation

**Technical Implementation**:
- Async message handling with FastAPI webhook endpoints
- Session state persistence in memory (conversation context)
- Validation service with exact regex patterns for phone, email, PIN, DOB
- Ticket generation service (format: `CS-YYYYMMDD-XXXXXX`)

### Data Models

**Primary Collections** (MongoDB/Beanie):
- `ComplaintDocument`: Cybercrime complaints with status tracking and history
- `UserDocument`: User accounts with encrypted passwords and RBAC
- `AuditLogDocument`: System action audit trail
- `CampaignDocument`: Awareness campaigns and notifications
- `AnalyticsEventDocument`: Event tracking for metrics

**Status Flow**:
Draft → Registered → Submitted to NCRP → Under Investigation → Escalated/Resolved/Closed

### API Design

**Architecture**: RESTful API with versioning (`/api/v1/`)

**Authentication**: Bearer token (JWT) in Authorization header

**Key Endpoints**:
- `/auth/*`: Login, registration, OAuth (Google)
- `/complaints/*`: CRUD operations with admin controls
- `/tracking/{reference_id}`: Public complaint tracking
- `/webhook/whatsapp`: WhatsApp message processing
- `/analytics/dashboard`: Dashboard statistics

**Error Handling**: Standardized HTTP status codes with JSON error responses

## External Dependencies

### Databases & Caching

**MongoDB Atlas** (Required):
- Cloud-hosted NoSQL database
- Free M0 tier available for development
- Connection via `MONGODB_URL` environment variable
- Used for all persistent data storage (users, complaints, audit logs)

**Redis** (Optional for production):
- In-memory cache and message broker
- Celery task queue backend
- Session storage for high-traffic scenarios

### Third-Party APIs

**WhatsApp Business API (Meta Cloud)**:
- Webhook-based message processing
- Required credentials: `META_ACCESS_TOKEN`, `META_PHONE_NUMBER_ID`, `META_VERIFY_TOKEN`
- API version: v18.0 (configurable)

**National Cybercrime Reporting Portal (NCRP)**:
- Integration endpoint: `cybercrime.gov.in/api`
- OAuth2 authentication with client credentials
- Mock mode available for development (`NCRP_MOCK_MODE=True`)
- Idempotency support for safe retries

**Google OAuth2** (Optional):
- Single Sign-On capability
- Requires `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
- Callback URL: `/api/v1/auth/google/callback`

**OpenAI API** (Optional):
- LLM chatbot for answering cybercrime questions
- Requires `OPENAI_API_KEY`
- Model: `gpt-3.5-turbo` (configurable via `LLM_MODEL`)
- Graceful fallback when unavailable

### Monitoring & Logging

**Sentry** (Optional):
- Error tracking and performance monitoring
- FastAPI integration via `sentry-sdk`
- Configured via `SENTRY_DSN` environment variable

**Prometheus** (Optional):
- Metrics collection with `prometheus-client`
- Custom metrics for complaint processing and API performance

### Email Service

**SMTP Configuration** (Optional):
- Email notifications for complaint status updates
- Admin alerts for escalations
- Configured via `SMTP_*` environment variables

### Deployment Platforms

**Replit**:
- Auto-detected configuration
- Uses Replit Secrets for sensitive environment variables
- Built-in webview proxy for frontend

**Vercel** (Frontend):
- Static site deployment from `frontend/dist`
- Configured via `vercel.json`
- API proxy to backend via rewrites

**Render.com / Railway.app** (Backend):
- Python web service deployment
- Auto-scaling with environment variables
- Health check endpoint: `/health`

### Python Dependencies

**Core Framework**:
- `fastapi==0.109.0`: Web framework
- `uvicorn[standard]==0.27.0`: ASGI server
- `pydantic>=2.5.2`: Data validation

**Database**:
- `motor==3.3.2`: Async MongoDB driver
- `beanie==1.24.0`: MongoDB ODM
- `pymongo==4.6.1`: MongoDB sync driver

**Security**:
- `PyJWT==2.8.0`: JWT token handling
- `cryptography==42.0.0`: Encryption operations
- `passlib==4.0.1`: Password hashing
- `bcrypt==4.0.1`: Bcrypt algorithm

**External APIs**:
- `httpx==0.26.0`: Async HTTP client
- `requests==2.31.0`: Sync HTTP client
- `aiohttp==3.9.1`: Alternative async HTTP

### JavaScript Dependencies

**Core**:
- `react==18.2.0`: UI library
- `react-dom==18.2.0`: DOM rendering
- `react-router-dom==6.14.0`: Routing

**Build Tools**:
- `vite==4.4.5`: Fast build tool
- `@vitejs/plugin-react==4.0.3`: React plugin
- `tailwindcss==3.3.3`: CSS framework

**Utilities**:
- `axios==1.4.0`: HTTP client
- `recharts==2.7.3`: Charts library
- `lucide-react==0.263.1`: Icon library