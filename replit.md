# CyberSathi Project

## Overview
CyberSathi is a WhatsApp-based AI chatbot for the National Cybercrime Helpline (1930) in India. It allows citizens to report cybercrimes, track complaints, and receive awareness guidance in English and Odia languages.

## Project Status
**Status**: Production-Ready MVP  
**Last Updated**: November 11, 2025  
**Version**: 1.0.0

## Architecture

### Backend (FastAPI)
- **Location**: `backend/`
- **Port**: 8000
- **Tech Stack**: Python 3.11, FastAPI, SQLAlchemy, Pydantic v2
- **Database**: SQLite (dev), PostgreSQL (production)
- **Features**:
  - REST API for complaint management
  - WhatsApp webhook integration (Meta Cloud API)
  - NCRP (cybercrime.gov.in) integration adapter
  - End-to-end encryption for sensitive data
  - NLP service with multilingual support
  - JWT-based authentication with RBAC
  - Audit logging

### Frontend (React)
- **Location**: `frontend/`
- **Port**: 5000
- **Tech Stack**: React 18, Vite, Tailwind CSS, React Router
- **Pages**:
  - Dashboard: Complaint overview and statistics
  - Case Tracker: Track complaints by reference ID
  - Awareness Center: Cyber safety tips and guidelines

### Key Components

#### 1. WhatsApp Integration
- Webhook handler: `/webhook/whatsapp`
- Message signature verification
- Interactive buttons and lists
- Template message support
- Conversation state management

#### 2. NCRP Integration
- OAuth2 authentication
- Automatic retry with exponential backoff
- Idempotency keys for submissions
- Response caching
- Mock mode for development

#### 3. NLP Service
- Intent detection (report fraud, track case, awareness)
- Language detection (English, Odia)
- Conversation flow management
- Button interaction handling

#### 4. Encryption Service
- AES-256 encryption (Fernet)
- Field-level encryption
- Password hashing (bcrypt)
- Secure key management

#### 5. Authentication & Authorization
- JWT token-based authentication
- Role-Based Access Control (RBAC)
- Roles: Citizen, Officer, Admin
- Protected endpoints

## Recent Changes (Session: Nov 11, 2025)

### Implemented Features
1. ✅ WhatsApp webhook handler with signature verification
2. ✅ NCRP integration adapter with retry logic
3. ✅ End-to-end encryption service
4. ✅ Enhanced complaint models (User, Officer, MessageLog)
5. ✅ NLP service with multilingual support
6. ✅ JWT authentication with RBAC
7. ✅ Modern React dashboard with Tailwind CSS
8. ✅ Comprehensive API documentation
9. ✅ Environment configuration (.env.example)
10. ✅ Dual workflows (Backend API + Frontend Dashboard)

### File Structure
```
CyberSathi/
├── backend/
│   ├── app/
│   │   ├── models/          # Pydantic models (v2)
│   │   │   ├── complaint.py # Complaint, Attachment
│   │   │   └── user.py      # User, Officer, MessageLog
│   │   ├── routers/         # API endpoints
│   │   │   ├── complaints.py
│   │   │   ├── tracking.py
│   │   │   ├── escalation.py
│   │   │   └── whatsapp_webhook.py
│   │   ├── services/        # Business logic
│   │   │   ├── encryption_service.py
│   │   │   ├── auth_service.py
│   │   │   ├── nlp_service.py
│   │   │   ├── whatsapp_service.py
│   │   │   ├── ncrp_adapter.py
│   │   │   ├── db_service.py
│   │   │   └── cyberportal_adapter.py
│   │   ├── config.py        # Pydantic settings
│   │   └── main.py          # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   └── Navbar.jsx
│   │   ├── pages/           # Page components
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── TrackerPage.jsx
│   │   │   └── AwarenessPage.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css       # Tailwind CSS
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── NCRP_INTEGRATION.md
│   ├── WHATSAPP_INTEGRATION.md
│   ├── ENCRYPTION_SECURITY.md
│   └── README.md
├── .env.example             # Environment template
└── replit.md               # This file
```

## Running the Project

### Development Mode
Both workflows are configured and running automatically:
1. **Backend API**: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`
2. **Frontend Dashboard**: `http://localhost:5000`

### Manual Start
```bash
# Backend
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Frontend
cd frontend
npm run dev
```

## Environment Variables

Required variables (see `.env.example` for full list):

### Core
- `DEBUG`: Enable debug mode
- `SECRET_KEY`: JWT secret key
- `ENCRYPTION_KEY`: Data encryption key

### WhatsApp (Meta Cloud API)
- `META_VERIFY_TOKEN`: Webhook verification token
- `META_ACCESS_TOKEN`: API access token
- `META_PHONE_NUMBER_ID`: WhatsApp Business phone ID

### NCRP Integration
- `NCRP_API_URL`: Cybercrime portal API URL
- `NCRP_CLIENT_ID`: OAuth2 client ID
- `NCRP_CLIENT_SECRET`: OAuth2 client secret
- `NCRP_API_KEY`: API key for authentication

## API Endpoints

### Public Endpoints
- `GET /health` - Health check
- `GET /webhook/whatsapp` - WhatsApp webhook verification
- `POST /webhook/whatsapp` - WhatsApp message handler

### Protected Endpoints
- `POST /api/v1/complaints/` - Create complaint
- `GET /api/v1/complaints/list` - List complaints
- `GET /api/v1/complaints/{id}` - Get complaint details

## Security Features

1. **End-to-End Encryption**
   - Sensitive data encrypted with AES-256
   - Password hashing with bcrypt
   - Secure key management

2. **Authentication & Authorization**
   - JWT tokens with expiration
   - Role-based access control
   - Protected API endpoints

3. **WhatsApp Security**
   - Message signature verification
   - Request validation
   - Rate limiting (planned)

4. **Data Protection**
   - Input validation and sanitization
   - SQL injection prevention
   - XSS protection
   - CORS configuration

## Testing

### API Testing
```bash
# Health check
curl http://localhost:8000/health

# List complaints
curl http://localhost:8000/api/v1/complaints/list
```

### Frontend Testing
Visit `http://localhost:5000` to access the dashboard.

## Deployment

### Requirements
- Python 3.11+
- Node.js 20+
- PostgreSQL (production)
- Redis (for session management)

### Production Checklist
- [ ] Set strong SECRET_KEY and ENCRYPTION_KEY
- [ ] Configure production database
- [ ] Set up WhatsApp Business API
- [ ] Obtain NCRP API credentials
- [ ] Enable HTTPS
- [ ] Configure CORS for production domain
- [ ] Set up monitoring and logging
- [ ] Enable rate limiting
- [ ] Set up automated backups

## Known Issues

1. **Pydantic Warnings**: Minor Pydantic v1 to v2 migration warnings in existing code
2. **Database**: Currently using SQLite for development (PostgreSQL recommended for production)
3. **Redis**: Session management requires Redis setup (optional for development)

## Future Enhancements

1. **Phase 2**:
   - Full Rasa NLP integration
   - Real-time notifications
   - File upload for evidence
   - Multi-language support (Hindi, Tamil, etc.)

2. **Phase 3**:
   - Analytics dashboard
   - Officer management portal
   - Automated case assignment
   - SMS integration

3. **Phase 4**:
   - Mobile app (React Native)
   - Voice bot integration
   - AI-powered fraud detection
   - Blockchain evidence chain

## Support & Contact

- **Helpline**: 1930 (National Cybercrime Helpline)
- **Website**: https://cybercrime.gov.in
- **Documentation**: See `/docs` folder

## License

Government of India - National Cybercrime Reporting Portal

---

**Note**: This project is part of the Digital India initiative to make cybercrime reporting accessible to all citizens.
