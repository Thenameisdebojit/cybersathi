# 🚀 CyberSathi - Local PC Setup Guide

This guide will help you run the CyberSathi application on your local computer (Windows, Mac, or Linux).

---

## ✅ Current Status

**Your app is now fully configured and running!**
- ✅ Frontend running on port 5000
- ✅ Backend running on port 8000
- ✅ In-memory database working (signup/login enabled)
- ✅ All dependencies installed

---

## 🔑 Default Login Credentials

Use these credentials to log in immediately:

```
Email: admin@cybersathi.in
Password: Admin@1930
```

---

## 📋 Prerequisites

Before running on your PC, make sure you have:

1. **Node.js 18+** - [Download here](https://nodejs.org/)
2. **Python 3.11+** - [Download here](https://www.python.org/)
   - ⚠️ During installation, check "Add Python to PATH"

---

## 🏃 Quick Start (Any Operating System)

### Step 1: Clone or Download the Project

Download this project to your computer.

### Step 2: Install Dependencies

**Frontend:**
```bash
cd frontend
npm install
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Start the Application

**Option A: Using Two Terminals (Recommended)**

Terminal 1 - Start Backend:
```bash
cd backend
python -m uvicorn app.main:app --host localhost --port 8000 --reload
```

Terminal 2 - Start Frontend:
```bash
cd frontend
npm run dev
```

**Option B: Windows Batch File**

Simply double-click `_start_app.bat` (if available)

### Step 4: Access the Application

Open your browser and go to:
- **Frontend:** http://localhost:5000
- **Backend API Docs:** http://localhost:8000/docs

---

## 💾 Database Options

### Current Setup: In-Memory Database

**How it works:**
- The app is currently using an in-memory database (mongomock)
- ✅ **Pros:** Works immediately, no setup required
- ⚠️ **Cons:** All data is lost when you restart the backend

**Who should use this:**
- Testing and development
- Quick demos
- Learning how the app works

### Permanent Storage: MongoDB Atlas (FREE)

To keep your data permanently, follow these steps:

#### 1. Create Free MongoDB Atlas Account

1. Go to https://www.mongodb.com/cloud/atlas
2. Click "Try Free"
3. Sign up with your email
4. Choose **FREE M0 Cluster** (512MB storage)
5. Select a cloud provider and region
6. Click "Create Cluster" (takes 3-5 minutes)

#### 2. Get Your Connection String

1. In MongoDB Atlas, click "Connect"
2. Choose "Connect your application"
3. Copy the connection string (looks like this):
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
   ```
4. Replace `<password>` with your actual password

#### 3. Update Configuration

Open `backend/.env` and update this line:

```env
MONGODB_URL=mongodb+srv://your-username:your-password@cluster0.xxxxx.mongodb.net/cybersathi?retryWrites=true&w=majority
```

#### 4. Restart the Backend

Stop the backend (Ctrl+C) and start it again. You'll see:
```
✅ MongoDB connection established successfully
```

Now your data will persist permanently!

---

## 🔧 Configuration Files

### Backend Environment Variables

All settings are in `backend/.env`:

```env
# Application Settings
DEBUG=True
PORT=8000
HOST=localhost

# Admin Credentials (change in production)
ADMIN_EMAIL=admin@cybersathi.in
ADMIN_PASSWORD=Admin@1930

# Database (update with your MongoDB Atlas URL)
MONGODB_URL=mongodb://localhost:27017

# File Upload
MAX_UPLOAD_SIZE_MB=10
LOCAL_STORAGE_PATH=data/uploads

# Optional: OpenAI API for AI Chatbot
# OPENAI_API_KEY=sk-your-openai-api-key-here
```

---

## 🧪 Testing the Application

### Test Signup

1. Go to http://localhost:5000/signup
2. Fill in the form:
   - Full Name: Test User
   - Email: test@example.com
   - Phone: +911234567890
   - Password: Test@1234
3. Click "Create Account"
4. ✅ You should be registered successfully

### Test Login

1. Go to http://localhost:5000/login
2. Enter credentials:
   - Email: admin@cybersathi.in
   - Password: Admin@1930
3. Click "Sign In"
4. ✅ You should be redirected to the dashboard

### Test API Directly

You can test the backend API at http://localhost:8000/docs

This opens interactive API documentation where you can test all endpoints.

---

## 🐛 Troubleshooting

### "Node.js is not installed"

**Solution:**
1. Download Node.js from https://nodejs.org/
2. Install it
3. Restart your terminal/command prompt
4. Run `node --version` to verify

### "Python is not installed"

**Solution:**
1. Download Python from https://www.python.org/
2. During installation, **check "Add Python to PATH"**
3. Restart your terminal/command prompt
4. Run `python --version` to verify

### "Port 5000 already in use"

**Solution:**
Either:
1. Stop any other app using port 5000
2. Or change the port in `frontend/vite.config.js`:
   ```js
   server: {
     port: 3000,  // Change to any free port
   }
   ```

### "Port 8000 already in use"

**Solution:**
1. Stop any other app using port 8000
2. Or change the port in `backend/.env`:
   ```env
   PORT=8001  # Change to any free port
   ```

### Frontend shows "Cannot connect to backend"

**Check:**
1. Is the backend running? (Check terminal)
2. Is it running on port 8000?
3. Any errors in the backend terminal?

**Fix:**
Make sure backend is started before frontend.

### Login/Signup not working

**Check backend logs for:**
1. Database connection errors
2. JWT secret key errors
3. Password hashing errors

**Common fixes:**
1. Make sure backend is running
2. Check `backend/.env` file exists
3. Restart the backend

### Database Connection Errors

**If you see:** "MongoDB connection refused"

**This is NORMAL with in-memory database!** The app automatically falls back to in-memory storage. Your app still works for testing.

**To fix permanently:** Set up MongoDB Atlas (see above)

---

## 📦 File Structure

```
cybersathi/
├── frontend/              # React frontend
│   ├── src/
│   │   ├── pages/         # Login, Signup, Dashboard, etc.
│   │   └── services/      # API calls
│   ├── package.json
│   └── vite.config.js
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── models/        # Database models
│   │   ├── routers/       # API routes
│   │   └── main.py        # Entry point
│   ├── .env               # Configuration (YOU EDIT THIS)
│   └── requirements.txt
└── LOCAL_SETUP_GUIDE.md   # This file
```

---

## 🎯 Next Steps

Now that your app is running:

1. **Explore the Dashboard** - Log in and see all features
2. **Test File Uploads** - Upload evidence files in complaints
3. **Try the AI Chatbot** - Click the chat bubble (bottom-right)
4. **Create Test Data** - Register complaints to test the system
5. **Set up MongoDB Atlas** - For permanent data storage

---

## 🌐 Deployment to Production

When you're ready to deploy:

1. **Change all secrets in `backend/.env`:**
   - Generate new SECRET_KEY and JWT_SECRET_KEY
   - Use strong passwords
   
2. **Set DEBUG=False** in backend/.env

3. **Deploy using:**
   - Replit Deployments (easiest)
   - Docker + Cloud VM
   - Vercel (frontend) + Railway (backend)

---

## 📞 Support

**Common Issues:**
- Check this guide's troubleshooting section
- Read error messages in terminal carefully
- Check `backend/.env` configuration

**Need Help?**
- Email: admin@cybersathi.in
- Helpline: 1930
- API Docs: http://localhost:8000/docs

---

## ⚙️ Advanced Configuration

### Enable AI Chatbot

1. Sign up at https://platform.openai.com
2. Create an API key
3. Add to `backend/.env`:
   ```env
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```
4. Restart backend
5. Chat button will now use AI

### Enable Email Notifications

Update `backend/.env`:
```env
EMAIL_SERVICE_API_KEY=your-sendgrid-api-key
EMAIL_FROM=noreply@cybersathi.in
```

### Enable WhatsApp Integration

Update `backend/.env`:
```env
META_ACCESS_TOKEN=your-whatsapp-business-token
META_PHONE_NUMBER_ID=your-phone-number-id
```

---

## 📊 System Requirements

**Minimum:**
- RAM: 4GB
- Storage: 2GB free space
- OS: Windows 10, macOS 10.14, Ubuntu 18.04 or newer

**Recommended:**
- RAM: 8GB
- Storage: 5GB free space
- SSD for better performance

---

**Built with ❤️ for India's Digital Safety**

© 2024 CyberSathi, Ministry of Home Affairs, Government of India
