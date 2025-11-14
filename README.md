# 🛡️ CyberSathi - Cybercrime Management System

![CyberSathi Banner](https://img.shields.io/badge/India-Cybercrime%20Management-blue?style=for-the-badge)
![License](https://img.shields.io/badge/Ministry-Home%20Affairs-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)

**CyberSathi** is India's premier cybercrime management application designed for law enforcement and government agencies. Built with PS-2 (Problem Statement 2) compliance, it provides a comprehensive platform for managing cybercrime complaints, tracking investigations, and supporting victims through an integrated AI chatbot.

---

## ✨ Features

### 🎯 Core Capabilities
- **Complaint Management** - Register, track, and resolve cybercrime complaints
- **Account Unfreeze Requests** - Process bank account unfreeze requests with supporting documents
- **Evidence Management** - Secure file uploads with support for images, videos, PDFs, and documents
- **Real-time Analytics** - Dashboard with complaint statistics and fraud trend analysis
- **AI-Powered Chatbot** - 24/7 automated support for cybercrime-related queries (powered by OpenAI)
- **Multi-channel Support** - WhatsApp, Web, and API integration ready

### 📊 PS-2 Compliance Features
- ✅ 13 mandatory reporter fields (name, email, phone, address, etc.)
- ✅ 23 financial fraud categories (UPI, Investment, Credit Card, etc.)
- ✅ Social media fraud tracking (Facebook, Instagram, WhatsApp, etc.)
- ✅ Evidence categorization and attachment system
- ✅ A/B/C/D menu workflow support
- ✅ Geographic complaint distribution tracking
- ✅ Resolution time analytics

### 🔐 Security & Compliance
- Bank-grade encryption for sensitive data
- Role-based access control (Admin, Officer, Viewer)
- Secure file storage with path traversal protection
- Audit logging for all operations
- Government data protection standards

---

## 🚀 Quick Start Guide

### Option 1: **Windows One-Click Startup** (Recommended)

The easiest way to run CyberSathi locally on Windows:

1. **Ensure Prerequisites are Installed:**
   - [Node.js 18+](https://nodejs.org/) (download and install)
   - [Python 3.11+](https://www.python.org/) (download and install)

2. **Double-Click the Batch File:**
   ```
   _start_app.bat
   ```

3. **That's It!** The script will:
   - ✅ Check if Node.js and Python are installed
   - ✅ Install frontend dependencies (npm install)
   - ✅ Install backend dependencies (pip install)
   - ✅ Create necessary directories (uploads folder)
   - ✅ Start backend server on http://localhost:8000
   - ✅ Start frontend server on http://localhost:5000
   - ✅ Open in separate command windows for easy monitoring

4. **Access the Application:**
   - **Frontend:** http://localhost:5000
   - **Backend API Docs:** http://localhost:8000/docs

5. **Default Credentials:**
   ```
   Email: admin@cybersathi.in
   Password: Admin@1930
   ```

---

### Option 2: Manual Startup

If you prefer manual control or are on macOS/Linux:

#### Backend Setup
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5000
```

---

### Option 3: Replit Cloud Deployment

Deploy to Replit for instant cloud hosting:

1. **Import Project** - Upload to Replit or connect GitHub repository
2. **Environment Variables** - Add in Replit Secrets:
   - `MONGODB_URL` - MongoDB Atlas connection string
   - `OPENAI_API_KEY` - OpenAI API key (optional, for AI chatbot)
3. **Run** - Click the Run button, both workflows start automatically
4. **Access** - Use the Replit webview to access your application

**Current Status:** ✅ Both frontend and backend workflows running in Replit

---

## ⚙️ Configuration

### Environment Variables

Create a `backend/.env` file with the following:

```env
# Database Configuration (Required for full functionality)
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/cybersathi?retryWrites=true&w=majority

# AI Chatbot (Optional - enables AI assistant)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Storage Configuration (Optional - defaults to local)
STORAGE_TYPE=local
LOCAL_STORAGE_PATH=./data/uploads

# S3 Storage (Optional - for cloud storage)
S3_ENDPOINT=https://s3.amazonaws.com
S3_BUCKET_NAME=cybersathi-uploads
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1

# Security (Automatically generated if not set)
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
```

### Getting Free Services

1. **MongoDB Atlas** (Free 512MB cluster):
   - Sign up at https://www.mongodb.com/cloud/atlas
   - Create a free cluster
   - Get your connection string
   - Add to `MONGODB_URL` in `.env`

2. **OpenAI API** (Pay-as-you-go, ~$0.002 per request):
   - Sign up at https://platform.openai.com
   - Create an API key
   - Add to `OPENAI_API_KEY` in `.env`

---

## 🏗️ Technology Stack

### Frontend
- **Framework:** React 18
- **Build Tool:** Vite 4.5
- **Routing:** React Router v6
- **Styling:** TailwindCSS 3.4
- **Icons:** Lucide React
- **HTTP Client:** Axios

### Backend
- **Framework:** FastAPI 0.109
- **Database:** MongoDB (Motor async driver)
- **Authentication:** JWT + OAuth2 (Google)
- **AI Integration:** OpenAI GPT-4o-mini
- **File Storage:** Local filesystem + S3 compatible
- **Validation:** Pydantic v2

### Infrastructure
- **Development:** Replit (cloud) + Local (Windows/Mac/Linux)
- **Database:** MongoDB Atlas
- **Object Storage:** S3 or Local filesystem
- **Deployment:** Replit Deployments, Docker, or VM

---

## 📁 Project Structure

```
cybersathi/
├── frontend/                    # React frontend application
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   │   ├── Logo.jsx        # CyberSathi logo component
│   │   │   ├── FloatingChatbot.jsx  # AI chatbot widget
│   │   │   └── Navbar.jsx      # Navigation bar
│   │   ├── pages/              # Page components
│   │   │   ├── LandingPage.jsx # Animated landing page
│   │   │   ├── NewLoginPage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   └── ComplaintsPage.jsx
│   │   ├── services/           # API services
│   │   └── App.jsx             # Main app with routing
│   ├── public/
│   │   └── assets/             # Static assets (logo, icons)
│   └── package.json
│
├── backend/                     # FastAPI backend
│   ├── app/
│   │   ├── models/             # Database models
│   │   │   ├── complaint.py    # Complaint & evidence models
│   │   │   ├── account_unfreeze.py
│   │   │   └── user.py
│   │   ├── api/                # API endpoints
│   │   │   ├── chatbot_ai.py   # AI chatbot endpoint
│   │   │   └── uploads.py      # File upload endpoint
│   │   ├── services/           # Business logic
│   │   │   └── storage_service.py
│   │   ├── database.py         # MongoDB connection
│   │   ├── config.py           # Configuration
│   │   └── main.py             # FastAPI app entry
│   └── requirements.txt
│
├── _start_app.bat              # Windows one-click startup
├── START_README.md             # Windows setup guide
├── README.md                   # This file
└── replit.md                   # Project documentation
```

---

## 🎨 User Interface

### Landing Page
- Animated gradient background with floating blobs
- CyberSathi logo prominently displayed
- Hero section with compelling messaging
- Statistics showcase (10,000+ complaints resolved, ₹50Cr+ recovered)
- Feature highlights (Security, Analytics, Multi-channel Support)
- Call-to-action buttons (Access Dashboard, Call 1930 Helpline)

### Admin Dashboard
- Real-time complaint statistics
- Fraud type distribution charts
- Recent complaints table
- Quick action buttons
- AI chatbot floating widget (bottom-right)

---

## 🤖 AI Chatbot Features

The integrated AI assistant can answer questions about:
- All 23 types of financial fraud
- Social media fraud prevention
- How to file complaints on cybercrime.gov.in
- Evidence collection and documentation
- Account freezing and unfreezing procedures
- Prevention tips and best practices

**To Enable:** Add `OPENAI_API_KEY` to your environment variables.

---

## 📞 Support & Resources

- **National Cybercrime Helpline:** 1930
- **Official Portal:** https://cybercrime.gov.in
- **Email Support:** support@cybersathi.in
- **API Documentation:** http://localhost:8000/docs (when running locally)

---

## 🐛 Troubleshooting

### "Node.js is not installed" Error
- Download and install Node.js from https://nodejs.org/
- Restart your terminal/command prompt
- Run `_start_app.bat` again

### "Python is not installed" Error
- Download and install Python 3.11+ from https://www.python.org/
- During installation, check "Add Python to PATH"
- Restart your terminal/command prompt
- Run `_start_app.bat` again

### Frontend or Backend Won't Start
- Check if ports 5000 and 8000 are already in use
- Close other applications using these ports
- Try restarting your computer

### MongoDB Connection Failed
- This is normal if you haven't configured MongoDB yet
- The app runs in "limited mode" without database
- To enable full features, add `MONGODB_URL` to `.env`

### AI Chatbot Not Working
- Ensure `OPENAI_API_KEY` is set in backend/.env
- Check your OpenAI account has credits
- The chatbot shows a clear error message if not configured

---

## 📝 License

© 2024 CyberSathi, Ministry of Home Affairs, Government of India.

This software is developed for government use in combating cybercrime. All rights reserved.

---

## 🙏 Acknowledgments

- **Ministry of Home Affairs, Government of India**
- **National Cybercrime Reporting Portal**
- **Indian Cyber Crime Coordination Centre (I4C)**
- **Law Enforcement Agencies** across India

---

## 📧 Contact

For technical support or feature requests:
- **Email:** admin@cybersathi.in
- **Helpline:** 1930
- **Website:** https://cybercrime.gov.in

---

**Built with ❤️ for India's Digital Safety**
