# CyberSathi Deployment Guide

This guide covers deploying the CyberSathi application to production.

## Table of Contents
- [Prerequisites](#prerequisites)
- [MongoDB Atlas Setup](#mongodb-atlas-setup)
- [Environment Configuration](#environment-configuration)
- [Vercel Deployment](#vercel-deployment)
- [Local Setup](#local-setup)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying, ensure you have:
- Node.js 18+ and Python 3.11+ installed
- A MongoDB Atlas account (free tier available)
- A Vercel account (optional, for deployment)
- WhatsApp Business API credentials (for chatbot functionality)

## MongoDB Atlas Setup

The application requires MongoDB as its database. Follow these steps to set up a free MongoDB Atlas cluster:

### Step 1: Create MongoDB Atlas Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for a free account
3. Create a new organization and project

### Step 2: Create a Cluster
1. Click "Build a Cluster"
2. Choose the FREE tier (M0 Sandbox)
3. Select your preferred cloud provider and region (choose one closest to your users)
4. Click "Create Cluster" (this may take 1-3 minutes)

### Step 3: Set Up Database Access
1. Navigate to "Database Access" in the left sidebar
2. Click "Add New Database User"
3. Create a username and strong password (save these securely!)
4. Under "Database User Privileges", select "Atlas admin"
5. Click "Add User"

### Step 4: Configure Network Access
1. Navigate to "Network Access" in the left sidebar
2. Click "Add IP Address"
3. For development: Click "Allow Access from Anywhere" (0.0.0.0/0)
4. For production: Add specific IP addresses or use cloud provider's IP ranges
5. Click "Confirm"

### Step 5: Get Connection String
1. Go to "Database" in the left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string (looks like: `mongodb+srv://username:<password>@cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority`)
5. Replace `<password>` with your database user password
6. Replace the database name with `cybersathi`

Example:
```
mongodb+srv://admin:YourPassword@cluster0.ab1cd.mongodb.net/cybersathi?retryWrites=true&w=majority
```

## Environment Configuration

### Backend Environment Variables

Create or update `backend/.env` with the following:

```env
# Application Settings
APP_NAME=CyberSathi
APP_VERSION=1.0.0
DEBUG=False
PORT=8000
HOST=0.0.0.0
FRONTEND_URL=https://your-frontend-domain.vercel.app
ENVIRONMENT=production

# MongoDB Database - IMPORTANT: Use your MongoDB Atlas connection string
MONGODB_URL=mongodb+srv://username:password@cluster.xxxxx.mongodb.net/cybersathi?retryWrites=true&w=majority
MONGODB_DB_NAME=cybersathi
MONGODB_MIN_POOL_SIZE=10
MONGODB_MAX_POOL_SIZE=100

# Security & JWT - Generate new keys for production!
SECRET_KEY=your_production_secret_key_min_32_chars
ENCRYPTION_KEY=your_production_encryption_key_32_bytes
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Admin Credentials
ADMIN_EMAIL=admin@cybersathi.in
ADMIN_PASSWORD=ChangeThisStrongPassword123!
ADMIN_PHONE=+919999999999

# WhatsApp Meta Cloud API (Required for chatbot)
META_VERIFY_TOKEN=your_verify_token
META_ACCESS_TOKEN=your_whatsapp_access_token
META_APP_SECRET=your_app_secret
META_PHONE_NUMBER_ID=your_phone_number_id
META_BUSINESS_ACCOUNT_ID=your_business_account_id
WHATSAPP_API_VERSION=v18.0

# NCRP Integration
NCRP_MOCK_MODE=True

# CORS
CORS_ORIGINS=https://your-frontend-domain.vercel.app
```

### Frontend Environment Variables

Create `frontend/.env.production`:

```env
VITE_API_URL=https://your-backend-domain.vercel.app/api/v1
```

## Deployment to Production

### ⚠️ Important: Backend Cannot Deploy to Vercel

**FastAPI (Python backend) cannot run on Vercel's serverless platform.** You need to deploy the backend separately.

### Recommended Backend Hosting Options:

#### Option 1: Render.com (Recommended - Free Tier Available)
1. Go to [Render.com](https://render.com)
2. Create new **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3.11+
5. Add all environment variables from `backend/.env.production.example`
6. Deploy - you'll get a URL like `https://cybersathi-api.onrender.com`

#### Option 2: Railway.app
1. Go to [Railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select backend directory
4. Add environment variables
5. Deploy

#### Option 3: DigitalOcean App Platform
1. Create new app on DigitalOcean
2. Deploy from GitHub
3. Set build and run commands
4. Add environment variables

### Frontend Deployment (Vercel)

#### Deploy Frontend via Vercel CLI:
```bash
cd frontend
npm install
npm run build
vercel --prod
```

### Option 2: Deploy via Vercel Dashboard

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Other
   - **Root Directory**: `backend` (for backend) or `frontend` (for frontend)
   - **Build Command**: 
     - Backend: `pip install -r requirements.txt`
     - Frontend: `npm install && npm run build`
   - **Output Directory**: 
     - Backend: `.`
     - Frontend: `dist`

5. Add Environment Variables:
   - Click "Environment Variables"
   - Add all variables from your `.env` file
   - Make sure to mark sensitive variables as "Secret"

6. Click "Deploy"

### Post-Deployment Steps

1. **Update CORS Settings**: Add your Vercel domain to `CORS_ORIGINS` in backend `.env`
2. **Update Frontend API URL**: Set `VITE_API_URL` to your backend Vercel URL
3. **Test Endpoints**: Visit `https://your-backend.vercel.app/docs` to test API
4. **Create Admin User**: The admin user will be created automatically on first startup

## Local Setup

### For Windows (using .bat file):

The error you encountered (`'vite' is not recognized`) occurs because npm dependencies aren't installed locally.

**Fix:**
```cmd
# Navigate to project root
cd D:\cybersathi

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies (using uv)
cd ..\backend
pip install -r requirements.txt

# Return to root and run the start script
cd ..
start_app.bat
```

### For Linux/Mac:

```bash
# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt

# Start the application
cd ..
chmod +x start_app.sh
./start_app.sh
```

### Using Docker (Alternative):

```bash
docker-compose up -d
```

## Troubleshooting

### Issue: MongoDB Connection Failed

**Solution:**
1. Verify your MongoDB Atlas connection string in `.env`
2. Check that your IP address is whitelisted in MongoDB Atlas Network Access
3. Ensure the database user password is correct
4. Test connection using MongoDB Compass or mongosh

### Issue: Vite Not Found (Local Development)

**Error:** `'vite' is not recognized as an internal or external command`

**Solution:**
```cmd
cd frontend
npm install
```

This installs all required npm packages including vite.

### Issue: CORS Errors

**Solution:**
1. Update `CORS_ORIGINS` in backend `.env` to include your frontend URL
2. Restart the backend server
3. Clear browser cache

### Issue: Authentication Not Working

**Solution:**
1. Verify `SECRET_KEY` is set in backend `.env`
2. Check that MongoDB is connected
3. Ensure admin user was created (check backend logs)
4. Clear localStorage in browser: `localStorage.clear()`

### Issue: WhatsApp Webhook Not Receiving Messages

**Solution:**
1. Verify `META_VERIFY_TOKEN` matches what you set in Meta Developer Console
2. Check that your webhook URL is publicly accessible (use ngrok for local testing)
3. Ensure webhook signature verification is passing
4. Check backend logs for webhook processing errors

## Production Checklist

Before going to production, ensure:

- [ ] MongoDB Atlas cluster is created and connection string is configured
- [ ] All environment variables are set in Vercel
- [ ] DEBUG=False in production environment
- [ ] SECRET_KEY and ENCRYPTION_KEY are secure and different from development
- [ ] CORS_ORIGINS only includes your production domains
- [ ] Admin password is strong and secure
- [ ] SSL/TLS is enabled (automatic with Vercel)
- [ ] WhatsApp Business API is configured and verified
- [ ] Tested complete user flows (signup, login, complaint submission)
- [ ] Database backups are configured in MongoDB Atlas
- [ ] Monitoring and error tracking is set up (optional: Sentry)

## Support

For issues or questions:
- Check the [Troubleshooting Guide](docs/Troubleshooting.md)
- Review [API Documentation](docs/API_DOCUMENTATION.md)
- Contact: admin@cybersathi.in

## Next Steps

After successful deployment:
1. Create admin user account
2. Configure WhatsApp Business webhook
3. Test complaint submission flow
4. Set up monitoring and alerts
5. Configure backup strategy
