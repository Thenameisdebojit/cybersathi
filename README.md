# CyberSathi - Cybercrime Complaint Management System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)](https://www.mongodb.com/cloud/atlas)

**CyberSathi** is India's premier cybercrime complaint management platform designed for government agencies and law enforcement. The system enables citizens to report cybercrimes via WhatsApp (1930 helpline), with a comprehensive admin dashboard for tracking, managing, and resolving complaints.

## 🚀 Quick Start

### Prerequisites
- **Python**: 3.11 or higher
- **Node.js**: 18 or higher  
- **MongoDB Atlas**: Cloud database (**REQUIRED** - free tier available)

> ⚠️ **IMPORTANT**: MongoDB Atlas is required for login, registration, and all data storage.

### Running on Replit

The application is already configured for Replit. Simply:

1. **Add MongoDB Atlas Connection**
   - The system will prompt you for `MONGODB_URL`
   - Follow the instructions to create a free MongoDB Atlas cluster
   - Paste your connection string when prompted

2. **Access the Application**
   - Frontend: Click the webview button in Replit
   - Backend API: `https://your-repl-url.replit.dev/docs`

3. **Default Login Credentials**
   ```
   Email:    admin@cybersathi.in
   Password: Admin@1930
   ```

### Running Locally

#### 1. Clone Repository
```bash
git clone <repository-url>
cd cybersathi
```

#### 2. Set Up MongoDB Atlas (REQUIRED)

**Get your FREE MongoDB connection string:**

1. Visit https://cloud.mongodb.com
2. Create a free account (no credit card needed)
3. Click "Create a New Cluster" → Select **M0 (Free Tier)**
4. Choose your region and click "Create Cluster"
5. Go to "Database Access" → Add a new database user with username and password
6. Go to "Network Access" → Click "Add IP Address" → Select "Allow Access from Anywhere" (for development)
7. Go back to "Database" → Click "Connect" → "Connect Your Application"
8. Copy the connection string (looks like):
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/cybersathi?retryWrites=true&w=majority
   ```
9. Replace `<username>` and `<password>` with your actual credentials

#### 3. Configure Backend Environment

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and update these **required** fields:
```bash
# MongoDB Atlas (REQUIRED)
MONGODB_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/cybersathi

# These are auto-generated, but you can customize them
SECRET_KEY=<your-secret-key>
ENCRYPTION_KEY=<your-encryption-key>

# Admin Credentials
ADMIN_EMAIL=admin@cybersathi.in
ADMIN_PASSWORD=Admin@1930
```

#### 4. Install Dependencies

**Windows:**
```cmd
# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ..\backend
pip install -r requirements.txt
pip install email-validator

# Return to root
cd ..
```

**Linux/Mac:**
```bash
# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt
pip install email-validator

# Return to root
cd ..
```

#### 5. Start Application

**Windows:**
```cmd
start_app.bat
```

**Linux/Mac:**
```bash
chmod +x start_app.sh
./start_app.sh
```

#### 6. Access the Application
- **Frontend Dashboard**: http://localhost:5000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 📋 Features

### Core Functionality
- ✅ **User Authentication**: Secure login and registration with JWT
- ✅ **MongoDB Integration**: All user data stored in MongoDB Atlas
- ✅ **Admin Dashboard**: Comprehensive complaint management interface
- ✅ **WhatsApp Integration**: Accept complaints via WhatsApp Business API
- ✅ **Multi-language Support**: English and Odia translations
- ✅ **Real-time Tracking**: Monitor complaint status updates
- ✅ **Secure & Compliant**: Bank-grade security with data encryption

### Technology Stack

#### Backend (FastAPI + Python)
- **FastAPI** - Modern, high-performance web framework
- **Motor + Beanie** - Async MongoDB ODM
- **PyJWT** - JWT authentication
- **Pydantic** - Data validation
- **Passlib + Bcrypt** - Password hashing

#### Frontend (React + Vite + Tailwind)
- **React 18** - UI library with hooks
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Lucide React** - Modern icon library

---

## 🏗️ Architecture

```
cybersathi/
├── backend/
│   ├── app/
│   │   ├── routers/          # API endpoints
│   │   │   ├── auth.py       # Authentication routes
│   │   │   ├── complaints.py # Complaint management
│   │   │   ├── tracking.py   # Status tracking
│   │   │   └── analytics.py  # Analytics & reports
│   │   ├── models/           # Database models
│   │   │   ├── user.py       # User document
│   │   │   ├── complaint.py  # Complaint document
│   │   │   └── audit_log.py  # Audit logging
│   │   ├── services/         # Business logic
│   │   │   ├── auth.py       # Auth service
│   │   │   ├── whatsapp_service.py
│   │   │   └── nlp_service.py
│   │   ├── i18n/             # Translations
│   │   ├── config.py         # Configuration
│   │   ├── database.py       # MongoDB connection
│   │   └── main.py           # FastAPI application
│   ├── .env.example          # Environment template
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── ui/          # Reusable UI components
│   │   │   └── ...
│   │   ├── pages/           # Page components
│   │   │   ├── NewLoginPage.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── ...
│   │   ├── services/        # API clients
│   │   │   ├── api.js       # Axios instance
│   │   │   └── auth.js      # Auth service
│   │   └── App.jsx          # Root component
│   ├── package.json         # npm dependencies
│   └── vite.config.js       # Vite configuration
└── README.md
```

---

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for secure password storage
- **PII Masking**: Automatic masking of sensitive data in logs
- **Input Validation**: Comprehensive validation for all user inputs
- **CORS Protection**: Configured for secure cross-origin requests
- **Environment Secrets**: Sensitive data stored in environment variables
- **MongoDB Atlas**: Cloud database with built-in security

---

## 📊 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - User logout
- `POST /api/v1/auth/change-password` - Change password

#### Complaints
- `GET /api/v1/complaints` - List all complaints
- `POST /api/v1/complaints` - Create new complaint
- `GET /api/v1/complaints/{id}` - Get complaint details
- `PUT /api/v1/complaints/{id}` - Update complaint
- `DELETE /api/v1/complaints/{id}` - Delete complaint

---

## 🌐 Environment Variables

### Required Variables

```bash
# Application
APP_NAME=CyberSathi
APP_VERSION=1.0.0
DEBUG=True

# MongoDB (REQUIRED)
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/cybersathi
MONGODB_DB_NAME=cybersathi

# Security (Auto-generated)
SECRET_KEY=<auto-generated-secret-key>
ENCRYPTION_KEY=<auto-generated-encryption-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin Credentials
ADMIN_EMAIL=admin@cybersathi.in
ADMIN_PASSWORD=Admin@1930
ADMIN_PHONE=+919999999999

# Frontend
FRONTEND_URL=http://localhost:5000
```

### Optional Variables

```bash
# WhatsApp Meta Cloud API
META_VERIFY_TOKEN=your_verify_token_here
META_ACCESS_TOKEN=your_whatsapp_access_token
META_PHONE_NUMBER_ID=your_phone_number_id

# NCRP Integration
NCRP_API_URL=https://cybercrime.gov.in/api
NCRP_MOCK_MODE=True

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

---

## 🧪 Testing

### Test User Registration
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test@1234",
    "full_name": "Test User",
    "phone": "+919999999999",
    "role": "viewer"
  }'
```

### Test Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@cybersathi.in",
    "password": "Admin@1930"
  }'
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Update MongoDB URL to production database
- [ ] Change ADMIN_PASSWORD to a strong password
- [ ] Generate new SECRET_KEY and ENCRYPTION_KEY
- [ ] Set DEBUG=False
- [ ] Configure WhatsApp Business API credentials
- [ ] Set up SSL/TLS certificates
- [ ] Configure reverse proxy (Nginx/Apache)
- [ ] Enable database backups
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting

---

## 📚 Documentation

- **API Documentation**: http://localhost:8000/docs (when running)
- **MongoDB Setup Guide**: See setup instructions above
- **Architecture Diagrams**: See docs folder
- **Security Documentation**: See docs/ENCRYPTION_SECURITY.md

---

## 🤝 Contributing

This is a government project for cybercrime management. Contributions are welcome for:

- Bug fixes
- Performance improvements
- Documentation enhancements
- Security patches
- Translation updates

---

## 📞 Support

For issues and questions:

1. Check API documentation at `/docs` endpoint
2. Review logs in console
3. Contact system administrator

---

## 📄 License

This project is developed for government use by the Ministry of Home Affairs, Government of India.

---

## 🏆 Credits

**CyberSathi Team**  
Ministry of Home Affairs, Government of India  
National Cybercrime Helpline: **1930**

---

**Built for a safer digital India** 🇮🇳
