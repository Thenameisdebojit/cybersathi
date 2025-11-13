# CyberSathi - Complete Setup Guide

## 🎉 What's Been Done

### ✅ Environment Configuration
- Created comprehensive `.env.example` file with all required environment variables
- Created `backend/.env` with development defaults
- Created `frontend/.env.example` for frontend configuration

### ✅ Batch Files Fixed
- Updated `start_app.bat` (Windows) to work in Replit environment
- Updated `start_app.sh` (Linux/Mac) with proper error handling
- Removed local MongoDB setup (using cloud MongoDB instead)

### ✅ Beautiful White & Green UI Theme
- Updated Tailwind config with professional green color palette (#2ECC71 primary)
- Implemented glassmorphism effects and modern shadows
- Added smooth animations and transitions
- Updated Navbar with gradient logo and sticky header
- Redesigned LoginPage with gradient backgrounds
- Enhanced DashboardPage with modern card designs
- Followed 2025 UI/UX best practices for million-user apps
- Ensured 44px minimum touch targets for accessibility
- Added responsive design support

### ✅ Vercel Deployment Configuration
- Created `vercel.json` for frontend deployment
- Configured proper routing and rewrites

### ✅ Dependencies Installed
- All frontend npm packages installed
- All backend Python packages installed
- Google OAuth libraries added

---

## 🚀 Next Steps to Get Your App Running

### 1. Set Up MongoDB Atlas (Required)

The app needs a cloud database. Here's how to set it up for FREE:

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up for a free account
3. Create a new cluster (select FREE tier)
4. Click "Connect" on your cluster
5. Create a database user with username and password
6. Whitelist your IP (or use `0.0.0.0/0` for development)
7. Get your connection string (should look like this):
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/cybersathi
   ```

8. Update `backend/.env` file:
   ```env
   MONGODB_URL=mongodb+srv://your-username:your-password@cluster0.xxxxx.mongodb.net
   MONGODB_DB_NAME=cybersathi
   ```

### 2. Start the Application

**Option A: Using the startup script (Recommended)**
```bash
./start_app.sh
```

**Option B: Manual start**

Terminal 1 (Backend):
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

### 3. Access the Application

- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 4. Default Login Credentials

```
Email: admin@cybersathi.in
Password: Admin@1930
```

⚠️ **Change these in production!**

---

## 🎨 UI/UX Improvements Made

### Color Palette
- **Primary Green**: #2ECC71 (Emerald)
- **Success Green**: #06D6A0 
- **Dark Green**: #145A32 (text)
- **White/Off-white**: #FFFFFF, #F8F9FA

### Modern Features
- ✨ Glassmorphism card effects
- 🎭 Smooth fade-in and slide-up animations
- 🎯 Gradient primary buttons
- 💫 Hover effects with shadow transitions
- 📱 Responsive design for all screen sizes
- ♿ WCAG 2.1 accessibility compliance
- 🌙 Dark mode ready (can be enabled later)

### Components Updated
- `Navbar`: Gradient logo, sticky header, modern navigation
- `LoginPage`: Gradient hero background, glass cards
- `DashboardPage`: Modern stat cards, success badges
- `App.jsx`: Subtle gradient background
- All buttons: Minimum 44px touch targets

---

## 📦 Deployment to Vercel

### Frontend Deployment

1. Push your code to GitHub
2. Go to [Vercel](https://vercel.com)
3. Import your GitHub repository
4. Configure build settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add environment variable:
   ```
   VITE_API_URL=your-backend-url-here
   ```
6. Deploy!

### Backend Deployment Options

**Option 1: Replit (Easiest)**
- Your backend is already on Replit
- Just click "Publish" in Replit to deploy
- Copy the deployed URL to Vercel's `VITE_API_URL`

**Option 2: Railway.app**
- Connect your GitHub repo
- Select `backend` as root directory
- Add all environment variables from `backend/.env`
- Deploy!

**Option 3: Render.com**
- Create new Web Service
- Connect GitHub repo
- Set build command: `cd backend && pip install -r requirements.txt`
- Set start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Add environment variables

---

## 🔧 Optional Configurations

### Google OAuth (Optional)
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add to `backend/.env`:
   ```env
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

### WhatsApp Integration (Optional)
1. Go to [Meta for Developers](https://developers.facebook.com)
2. Create WhatsApp Business App
3. Get credentials and add to `backend/.env`

---

## 🐛 Troubleshooting

### Backend won't start
- ✅ Make sure MongoDB Atlas is configured in `backend/.env`
- ✅ Check connection string format
- ✅ Verify network access in MongoDB Atlas (whitelist IPs)

### Frontend shows connection errors
- ✅ Make sure backend is running first
- ✅ Check proxy configuration in `frontend/vite.config.js`
- ✅ Verify CORS settings in backend

### Port already in use
```bash
# Kill processes on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill processes on port 5000 (frontend)
lsof -ti:5000 | xargs kill -9
```

---

## 📚 Project Structure

```
cybersathi/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── config.py        # Configuration (updated)
│   │   ├── database.py      # MongoDB connection
│   │   ├── models/          # Database models
│   │   ├── routers/         # API endpoints
│   │   └── services/        # Business logic
│   ├── .env                 # Backend environment (created)
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components (updated)
│   │   ├── pages/           # Page components (updated)
│   │   ├── styles.css       # Global styles (updated)
│   │   └── App.jsx          # Main app (updated)
│   ├── tailwind.config.js   # Tailwind config (updated)
│   ├── vite.config.js       # Vite config
│   └── package.json         # npm dependencies
├── .env.example             # Environment template (created)
├── vercel.json              # Vercel config (created)
├── start_app.sh             # Startup script (fixed)
└── start_app.bat            # Windows startup (fixed)
```

---

## 🎯 Key Features

- **Authentication**: JWT-based with Google OAuth support
- **Complaint Management**: Full CRUD for cybercrime reports
- **Analytics Dashboard**: Real-time statistics
- **WhatsApp Integration**: Automated chatbot responses
- **Admin Panel**: User and complaint management
- **Scalable Architecture**: MongoDB, Redis, Celery

---

## 💡 Tips

1. **Development**: Use the default `.env` file for local testing
2. **Production**: Always change `SECRET_KEY`, `ADMIN_PASSWORD`, and other sensitive values
3. **Security**: Never commit `.env` files to version control
4. **Backups**: MongoDB Atlas provides automatic backups
5. **Monitoring**: Consider adding Sentry DSN for error tracking

---

## 📞 Support

If you encounter issues:
1. Check this guide first
2. Review error messages in terminal
3. Check backend logs at `http://localhost:8000`
4. Verify all environment variables are set correctly

---

## 🚀 You're All Set!

Just configure MongoDB Atlas and run `./start_app.sh` to get started!

**Happy coding! 💚**
