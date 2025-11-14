# 🧪 Local Deployment Verification Checklist

This document provides a comprehensive test to ensure CyberSathi runs correctly on your local machine.

---

## ✅ Pre-Deployment Checks

### 1. System Requirements
- [ ] **Node.js 18+** installed
  ```bash
  node --version
  # Should show v18.x.x or higher
  ```

- [ ] **Python 3.11+** installed
  ```bash
  python --version
  # Should show Python 3.11.x or higher
  ```

- [ ] **Git** installed (optional, for version control)
  ```bash
  git --version
  ```

---

## 🚀 Quick Start Test (Windows)

### Method 1: Using BAT File (Recommended)

1. **Open File Explorer** and navigate to project folder
2. **Double-click** `_start_app.bat`
3. **Wait** for installation and startup (first run takes 2-5 minutes)
4. **Verify** two command windows open:
   - "CyberSathi Backend" - Shows backend logs
   - "CyberSathi Frontend" - Shows frontend logs

### Expected Output:

**Backend Window:**
```
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXX] using WatchFiles
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
🚀 Starting CyberSathi Backend...
🌟 CyberSathi v1.0.0 is ready!
📊 API Docs: http://0.0.0.0:8000/docs
```

**Frontend Window:**
```
  VITE v4.5.14  ready in XXX ms

  ➜  Local:   http://localhost:5000/
  ➜  Network: http://YOUR_IP:5000/
  ➜  press h to show help
```

---

## 🧪 Manual Test (All Platforms)

### Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Create .env file (optional - works without it)
cp .env.example .env

# Start backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**✅ Success Indicators:**
- ✅ No import errors
- ✅ "CyberSathi v1.0.0 is ready!" message
- ✅ Accessible at http://localhost:8000

### Step 2: Frontend Setup (New Terminal)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start frontend
npm run dev -- --host 0.0.0.0 --port 5000
```

**✅ Success Indicators:**
- ✅ Vite compiles without errors
- ✅ "ready in X ms" message
- ✅ Accessible at http://localhost:5000

---

## 🔍 Functionality Tests

### Test 1: Landing Page ✅
1. **Open** http://localhost:5000
2. **Verify** you see:
   - ✅ CyberSathi logo in top-left
   - ✅ Blue gradient animated background
   - ✅ "Protect Citizens. Fight Cybercrime." heading
   - ✅ Statistics: 10,000+, ₹50Cr+, 24/7, 500+
   - ✅ "Access Dashboard" button
   - ✅ "Call 1930 Helpline" button

### Test 2: Login Page ✅
1. **Click** "Sign In" or "Access Dashboard"
2. **Verify** you see:
   - ✅ Login form with email and password fields
   - ✅ "Sign up here" link
   - ✅ "Forgot password?" link
   - ✅ CyberSathi branding on left side

### Test 3: Backend API ✅
1. **Open** http://localhost:8000
2. **Verify** you see:
   - ✅ JSON response: `{"message": "CyberSathi API v1.0.0", "status": "operational"}`

### Test 4: API Documentation ✅
1. **Open** http://localhost:8000/docs
2. **Verify** you see:
   - ✅ Swagger/OpenAPI interactive documentation
   - ✅ Available endpoints listed
   - ✅ Can test endpoints directly

### Test 5: Health Check ✅
1. **Open** http://localhost:8000/health
2. **Verify** you see:
   - ✅ JSON with status, version, database status
   - ✅ `"status": "healthy"` or `"status": "limited_mode"`

### Test 6: AI Chatbot (if OPENAI_API_KEY is set) ✅
1. **Go to** http://localhost:5000 (while logged in)
2. **Click** the blue chatbot icon (bottom-right)
3. **Type** "What is UPI fraud?"
4. **Verify**:
   - ✅ Chatbot opens with CyberSathi branding
   - ✅ Response appears (if API key set)
   - ✅ OR error message about missing API key (if not set)

---

## 🐛 Common Issues & Solutions

### Issue 1: "Node.js is not installed"
**Solution:**
1. Download from https://nodejs.org/ (LTS version)
2. Install with default settings
3. Restart command prompt
4. Run `_start_app.bat` again

---

### Issue 2: "Python is not installed"
**Solution:**
1. Download from https://www.python.org/ (Python 3.11+)
2. ⚠️ **IMPORTANT:** Check "Add Python to PATH" during installation
3. Restart command prompt
4. Run `_start_app.bat` again

---

### Issue 3: "Port 5000 already in use"
**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>
```

---

### Issue 4: "Port 8000 already in use"
**Solution:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Mac/Linux
lsof -i :8000
kill -9 <PID>
```

---

### Issue 5: "MongoDB connection failed"
**Expected Behavior:**
- ⚠️ This is NORMAL if you haven't set up MongoDB
- The app runs in "limited mode" without database
- All UI features work, but data is not persisted

**To Fix (Optional):**
1. Get free MongoDB Atlas: https://www.mongodb.com/cloud/atlas
2. Create cluster and get connection string
3. Add to `backend/.env`:
   ```
   MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/cybersathi
   ```
4. Restart backend

---

### Issue 6: "AI Chatbot not responding"
**Expected Behavior:**
- ⚠️ Chatbot shows error if OPENAI_API_KEY not set
- This is NORMAL - the app works without it

**To Fix (Optional):**
1. Get API key: https://platform.openai.com/api-keys
2. Add to `backend/.env`:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
3. Restart backend

---

### Issue 7: Frontend build errors
**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

### Issue 8: Backend import errors
**Solution:**
```bash
cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 📊 Test Results Summary

After running all tests, fill this out:

| Test | Status | Notes |
|------|--------|-------|
| Node.js installed | ✅ / ❌ | Version: ______ |
| Python installed | ✅ / ❌ | Version: ______ |
| Backend starts | ✅ / ❌ | Port: 8000 |
| Frontend starts | ✅ / ❌ | Port: 5000 |
| Landing page loads | ✅ / ❌ | Logo visible |
| Login page loads | ✅ / ❌ | Form works |
| Backend API responds | ✅ / ❌ | JSON returned |
| API docs accessible | ✅ / ❌ | Swagger UI |
| Chatbot appears | ✅ / ❌ | Icon visible |
| MongoDB connected | ✅ / ❌ / N/A | Optional |
| OpenAI working | ✅ / ❌ / N/A | Optional |

---

## ✅ Success Criteria

Your local deployment is successful if:

**Minimum Requirements (Core Functionality):**
- ✅ Backend starts without critical errors
- ✅ Frontend starts and compiles successfully
- ✅ Landing page loads with logo visible
- ✅ Login page is accessible
- ✅ API documentation at /docs works

**Optional (Enhanced Features):**
- ✅ MongoDB connected (for data persistence)
- ✅ OpenAI API key set (for AI chatbot)
- ✅ All UI pages navigate correctly

**Note:** MongoDB and OpenAI are OPTIONAL. The app is fully functional without them, it just operates in "limited mode" without data persistence and AI features.

---

## 🎯 Next Steps After Successful Deployment

1. **Add MongoDB** (if you want to save data):
   - Sign up at https://www.mongodb.com/cloud/atlas
   - Get free 512MB cluster
   - Add connection string to `.env`

2. **Add OpenAI** (if you want AI chatbot):
   - Sign up at https://platform.openai.com
   - Get API key (starts with sk-)
   - Add to `.env`

3. **Create admin account**:
   - Login with: admin@cybersathi.in / Admin@1930
   - Or register a new account at signup page

4. **Explore features**:
   - Dashboard analytics
   - Complaint management
   - Evidence uploads
   - User management

---

## 🆘 Still Having Issues?

If you've followed all steps and tests but still facing issues:

1. **Check the console logs** in both terminal windows
2. **Look for red ERROR messages**
3. **Copy the error message**
4. **Search for the error online** or contact support

**Support Contacts:**
- Email: admin@cybersathi.in
- Helpline: 1930
- GitHub Issues: (if repository is public)

---

**Last Updated:** November 14, 2024
**Version:** 1.0.0
