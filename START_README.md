# CyberSathi - Complete Startup Guide

## For Replit (Current Environment)

The app is already running! Just click the webview or visit the URL shown above.

- **Frontend**: Automatically running on port 5000
- **Backend**: Automatically running on port 8000
- **Login**: admin@cybersathi.in / Admin@1930

### To restart workflows:
Use the Replit interface or the restart buttons in the tools panel.

---

## For Windows Local Development

### Prerequisites
1. **Node.js** (v18 or higher) - https://nodejs.org/
2. **Python** (3.11) - https://www.python.org/
3. **Git** (optional) - https://git-scm.com/

### Quick Start (Recommended)

Simply double-click `_start_app.bat`

This script will:
1. Check if Node.js and Python are installed
2. Install all frontend dependencies (npm install)
3. Install all backend dependencies (pip install)
4. Create environment file if needed
5. Start both backend and frontend servers
6. Open in separate windows

### Manual Start

If the automated script doesn't work, follow these steps:

#### Terminal 1 - Backend
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host localhost --port 8000 --reload
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm install
npm run dev
```

### Environment Configuration

1. Copy `backend/.env.example` to `backend/.env`
2. Edit `backend/.env` and add your API keys:

**Required for AI Chatbot:**
```
OPENAI_API_KEY=sk-your-openai-api-key-here
```
Get your key from: https://platform.openai.com/api-keys

**Optional but recommended:**
```
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net
```
Get free MongoDB Atlas cluster from: https://www.mongodb.com/cloud/atlas

### Access the Application

Once both servers are running:

- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

**Default Login:**
- Email: `admin@cybersathi.in`
- Password: `Admin@1930`

---

## Features Included

### ✅ Core Features
- User Authentication (Email/Password + Google OAuth)
- Complaint Management System
- WhatsApp Chatbot Integration
- Status Tracking
- Role-based Access Control
- Analytics Dashboard

### ✅ PS-2 Compliant Features
- **23 Financial Fraud Types** (Investment, UPI, APK, Job Fraud, etc.)
- **Social Media Fraud Types** (Facebook, Instagram, WhatsApp, etc.)
- **Complete Reporter Information** (13 required fields)
- **Evidence Upload** (Multiple file types supported)
- **Account Unfreeze Requests**
- **Status Check** (by acknowledgement number or phone)
- **Export to CSV/Excel**

### ✅ New Features Added
- **Floating AI Chatbot** - Ask questions about cybercrime (uses OpenAI GPT-4)
- **Integrated Logo** - CyberSathi shield logo throughout the app
- **File Upload System** - S3-compatible with local fallback
- **Enhanced Security** - PII encryption and secure storage

---

## Troubleshooting

### Backend fails to start
- **Error**: "Failed to connect to MongoDB"
  - **Solution**: This is normal if MongoDB is not configured. The app runs in limited mode without database.
  - **To fix**: Add MONGODB_URL to backend/.env with your MongoDB Atlas connection string.

- **Error**: "Module not found"
  - **Solution**: Run `cd backend && python -m pip install -r requirements.txt`

### Frontend fails to start
- **Error**: "vite: not found"
  - **Solution**: Run `cd frontend && npm install`

- **Error**: Port already in use
  - **Solution**: Kill the process using the port or change ports in vite.config.js

### AI Chatbot not working
- **Error**: "Failed to process chat request"
  - **Cause**: Missing OPENAI_API_KEY
  - **Solution**: Add your OpenAI API key to backend/.env

### Windows: "Python not found"
- Make sure Python is added to PATH during installation
- Try running: `py` instead of `python`

---

## Project Structure

```
cybersathi/
├── backend/              # FastAPI Backend
│   ├── app/
│   │   ├── api/          # NEW: API endpoints (uploads, chatbot)
│   │   ├── models/       # Database models
│   │   ├── routers/      # API routers
│   │   ├── services/     # Business logic
│   │   └── main.py       # Application entry
│   ├── requirements.txt  # Python dependencies
│   └── .env.example      # Environment template
│
├── frontend/             # React Frontend
│   ├── src/
│   │   ├── components/   # NEW: FloatingChatbot, Logo
│   │   ├── pages/        # Application pages
│   │   └── App.jsx       # Main app component
│   ├── public/
│   │   └── assets/       # NEW: Logo files (SVG/PNG)
│   └── package.json      # Node dependencies
│
├── data/                 # Local file uploads
├── _start_app.bat        # Windows startup script
└── START_README.md       # This file
```

---

## Support

For issues or questions:
1. Check the logs in the terminal windows
2. Visit API docs at http://localhost:8000/docs
3. Check browser console for frontend errors
4. Ensure all environment variables are set correctly

**National Cybercrime Helpline: 1930**
