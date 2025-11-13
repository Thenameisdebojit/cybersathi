# CyberSathi - Cybercrime Helpline Assistant

## Overview

CyberSathi is an intelligent WhatsApp-based chatbot system designed to assist Indian citizens in reporting cybercrimes and interfacing with India's National Cybercrime Reporting Portal (1930 Helpline). The system provides a multi-language interface for complaint registration, real-time case tracking, and seamless integration with the official cybercrime.gov.in portal.

**Core Purpose**: Bridge the gap between citizens and cybercrime reporting by providing an accessible, WhatsApp-based interface that handles complaint registration, tracks case status, and integrates with national cybercrime infrastructure.

**Key Features**:
- Multi-language support (English, Hindi, Odia)
- WhatsApp Business API integration for complaint submission
- NLP-powered conversational assistance
- Real-time complaint tracking via reference IDs
- MongoDB-based data storage with encryption
- Role-based access control (RBAC) with 5 user roles
- Admin dashboard for case management
- National Cybercrime Reporting Portal (NCRP) integration
- Professional white and green UI theme (#2ECC71 emerald green, #A8E6CF mint accents)

## Recent Changes (November 13, 2025)

**Deployment Readiness**:
- ✅ Fixed all Python dependencies (email-validator, google-auth packages)
- ✅ Implemented professional white-green color theme across all frontend components
- ✅ Created comprehensive .env.example with all required environment variables
- ✅ Fixed backend configuration using Pydantic Field with validation_alias
- ✅ Added MongoDB startup guard for graceful degradation (starts in "limited mode" without database)
- ✅ Configured vercel.json with proper @vercel/static-build configuration
- ✅ Both backend and frontend workflows running successfully

**Configuration**:
- Backend starts successfully even without MongoDB connection (shows helpful warnings)
- CORS and file upload settings now properly configurable via environment variables
- Ready for deployment to Replit (backend) and Vercel (frontend)

**Next Steps**:
- Configure MongoDB Atlas connection string in backend/.env (MONGODB_URL)
- Update vercel.json with actual backend URL after Replit deployment
- Run full test suites with production credentials

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### 1. Backend Architecture (FastAPI + MongoDB)

**Framework**: FastAPI (Python 3.x) with async/await support for high-performance API operations.

**Design Pattern**: RESTful API with layered architecture:
- **Routers Layer**: API endpoint definitions (`/api/v1/auth`, `/api/v1/complaints`, `/api/v1/tracking`)
- **Services Layer**: Business logic (auth, NLP, WhatsApp, NCRP adapter)
- **Models Layer**: Beanie ODM documents for MongoDB
- **Database Layer**: MongoDB connection management with Motor (async driver)

**Key Architectural Decisions**:

1. **MongoDB with Beanie ODM**: Chosen over traditional SQL for flexible schema design needed for varying complaint types and multi-language content. Beanie provides async ORM capabilities with automatic indexing.
   - **Pros**: Schema flexibility, horizontal scalability, native JSON support for complex nested data
   - **Cons**: No ACID transactions across collections (mitigated by single-document atomicity)

2. **Async/Await Pattern**: All database and external API operations use async patterns to handle concurrent WhatsApp webhook requests efficiently.
   - **Requirement**: Handle multiple simultaneous user conversations via WhatsApp
   - **Solution**: Async FastAPI with Motor (async MongoDB driver)

3. **JWT Authentication**: Stateless token-based auth with access/refresh token pattern for admin dashboard and API access.
   - **Implementation**: `python-jose` for JWT, `bcrypt` for password hashing
   - **Security Features**: Failed login tracking (auto-lock after 5 attempts), role-based access control

4. **Modular Service Architecture**: Clear separation of concerns:
   - `auth.py`: User authentication and authorization
   - `nlp_service.py`: Conversation state management and message processing
   - `whatsapp_service.py`: Meta Cloud API integration
   - `ncrp_adapter.py`: National Cybercrime Portal integration
   - `cyberportal_adapter.py`: Legacy adapter (being replaced by ncrp_adapter)

### 2. Frontend Architecture (React + Vite)

**Framework**: React 18 with Vite build tool for fast development and optimized production builds.

**UI Library**: Tailwind CSS for utility-first styling with custom design system.

**Key Components**:
- Admin Dashboard for complaint management
- Real-time analytics and reporting
- Case tracking interface

**Build Configuration**:
- Development server on port 5000 with HMR (Hot Module Replacement)
- Proxy configuration to backend API (port 8000) to avoid CORS issues
- Production builds output to `dist/` directory

**Design Pattern**: Component-based architecture with React Router for navigation.

### 3. Data Storage Architecture

**Primary Database**: MongoDB (via Motor async driver + Beanie ODM)

**Collections/Documents**:
1. **ComplaintDocument**: Core complaint data with status tracking, attachments, location
   - Indexes: `reference_id`, `phone`, `status`, `created_at`
   - Features: Status history tracking, encrypted sensitive fields
   
2. **UserDocument**: Authentication and RBAC
   - Roles: super_admin, admin, officer, viewer, api_user
   - Features: Failed login tracking, password hashing with bcrypt
   
3. **AuditLogDocument**: Compliance and security audit trail
   - Tracks: User actions, complaint changes, security events
   
4. **CampaignDocument**: Awareness campaigns and notifications
   - Features: Target audience segmentation, delivery tracking
   
5. **AnalyticsEventDocument**: Real-time metrics and insights
   - Events: complaint_registered, user_interaction, whatsapp_message

**Connection Pooling**: Configured for 10-100 concurrent connections to handle production load.

**Encryption**: Field-level encryption using Fernet (AES-256) for sensitive PII data (phone numbers, bank details).

### 4. Authentication & Authorization

**Authentication Mechanism**: JWT-based with dual token approach
- **Access Token**: Short-lived (default 60 minutes), carries user context
- **Refresh Token**: Long-lived (default 7 days), used to obtain new access tokens

**Authorization**: Role-Based Access Control (RBAC) with 5 distinct roles:
- `super_admin`: Full system access
- `admin`: Manage complaints and users
- `officer`: Handle assigned cases
- `viewer`: Read-only access
- `api_user`: Programmatic access for integrations

**Security Features**:
- Password hashing with bcrypt (cost factor configurable)
- Failed login attempt tracking with account lockout
- Audit logging for all authentication events
- JWT signature verification on every protected endpoint

### 5. WhatsApp Integration Architecture

**Provider**: Meta Cloud API (WhatsApp Business API)

**Integration Pattern**: Webhook-based bidirectional communication:
1. **Inbound**: Meta sends POST requests to `/webhook/whatsapp` on user messages
2. **Outbound**: System sends messages via Meta Graph API

**Message Flow**:
```
User → WhatsApp → Meta Cloud API → Webhook → NLP Service → Response → Meta API → WhatsApp → User
```

**Components**:
- `whatsapp_service.py`: Outbound message sending (text, interactive buttons)
- `whatsapp_webhook.py`: Inbound webhook handler with signature verification
- `nlp_service.py`: Conversation state management and intent detection

**Security**: HMAC-SHA256 signature verification on all incoming webhooks using `META_APP_SECRET`.

**Conversation State**: In-memory session management tracking user flow through complaint registration stages.

### 6. External Service Integrations

**National Cybercrime Reporting Portal (NCRP)**:
- **Purpose**: Submit registered complaints to official government portal
- **Authentication**: OAuth2 client credentials flow
- **Implementation**: `ncrp_adapter.py` with retry logic and exponential backoff
- **Features**: Idempotency keys to prevent duplicate submissions, response caching
- **Mock Mode**: Development testing without live API calls

**Background Task Processing**:
- **Celery**: Configured for async task processing (complaint submission, notifications)
- **Broker**: Redis (separate database from cache)
- **Scheduler**: APScheduler for periodic tasks (status sync, campaign delivery)

**Monitoring & Observability**:
- **Prometheus**: Metrics export (configured but implementation pending)
- **Sentry**: Error tracking and performance monitoring
- **Structured Logging**: JSON logs for production environments

## External Dependencies

### Third-Party Services

1. **Meta Cloud API (WhatsApp Business)**
   - **Purpose**: WhatsApp messaging interface
   - **Authentication**: Bearer token (`META_ACCESS_TOKEN`)
   - **Endpoints**: Graph API v18.0
   - **Rate Limits**: Per Meta's cloud API limits
   - **Configuration**: `META_PHONE_NUMBER_ID`, `META_BUSINESS_ACCOUNT_ID`

2. **National Cybercrime Reporting Portal (cybercrime.gov.in)**
   - **Purpose**: Official complaint submission
   - **Authentication**: OAuth2 + API Key
   - **Base URL**: Configurable via `NCRP_API_URL`
   - **Credentials**: `NCRP_CLIENT_ID`, `NCRP_CLIENT_SECRET`, `NCRP_API_KEY`

3. **Redis**
   - **Purpose**: Caching and Celery message broker
   - **Databases**: 
     - DB 0: Application cache
     - DB 1: Celery broker
     - DB 2: Celery results backend
   - **Connection**: `REDIS_URL` (default: `redis://localhost:6379`)

4. **MongoDB**
   - **Purpose**: Primary data store
   - **Connection**: `MONGODB_URL` (default: `mongodb://localhost:27017`)
   - **Database**: `MONGODB_DB_NAME` (default: `cybersathi`)
   - **Driver**: Motor (async) + Beanie (ODM)

### Python Package Dependencies

**Core Framework**:
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `pydantic`: Data validation and settings management

**Database**:
- `motor`: Async MongoDB driver
- `beanie`: MongoDB ODM with async support
- `pymongo`: Sync MongoDB driver (fallback)

**Authentication & Security**:
- `python-jose`: JWT token handling
- `passlib`: Password hashing
- `bcrypt`: Hashing algorithm
- `cryptography`: Encryption utilities

**Background Tasks**:
- `celery`: Distributed task queue
- `redis`: Python Redis client
- `apscheduler`: Scheduled task execution

**External APIs**:
- `httpx`: Async HTTP client
- `requests`: Sync HTTP client
- `aiohttp`: Alternative async HTTP

**Testing**:
- `pytest`: Test framework
- `pytest-asyncio`: Async test support
- `faker`: Test data generation

### Frontend Dependencies

**Core**:
- `react`: UI library (v18.2.0)
- `react-dom`: React DOM rendering
- `react-router-dom`: Client-side routing

**UI Components**:
- `lucide-react`: Icon library
- `recharts`: Charts and analytics visualization
- `tailwindcss`: Utility-first CSS framework

**API Communication**:
- `axios`: HTTP client with interceptors

**Build Tools**:
- `vite`: Fast build tool and dev server
- `@vitejs/plugin-react`: React support for Vite

### Development Tools

**Linting**: ESLint with React plugins
**CSS Processing**: PostCSS with Autoprefixer
**Environment Management**: `python-dotenv` for configuration