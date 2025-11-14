# .env Configuration Guide

## Quick Reference

Your `backend/.env` file has been configured with defaults for development. Here's what you need to know:

## 🔴 REQUIRED (App Won't Work Without This)

### 1. MongoDB Atlas - **CRITICAL**
```env
MONGODB_URL=mongodb://localhost:27017  # ⚠️ REPLACE THIS!
```

**Status**: ❌ Not configured  
**Action**: Follow [MONGODB_SETUP.md](MONGODB_SETUP.md) to get your FREE MongoDB Atlas URL  
**Time**: 5 minutes  
**Why**: The app stores all user accounts, complaints, and data in MongoDB

**After setup, replace with:**
```env
MONGODB_URL=mongodb+srv://username:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/cybersathi?retryWrites=true&w=majority
```

## 🟢 CONFIGURED (Ready to Use)

### 1. Admin Account
```env
ADMIN_EMAIL=admin@cybersathi.in
ADMIN_PASSWORD=Admin@1930
```
**Status**: ✅ Configured  
**Default Login**: Use these credentials after MongoDB is set up

### 2. Security Keys
```env
SECRET_KEY=J0JedtFHqIuWeTkG_aiOE9JLX4uG-AFQyji-BffNoBI
ENCRYPTION_KEY=FP50e7F13iwHWi4fDwHFZJNZ9dMy4BZXI6Kds3v7kVA=
```
**Status**: ✅ Configured  
**Note**: These are development keys. Generate new ones for production.

### 3. Application Settings
```env
DEBUG=True
PORT=8000
FRONTEND_URL=http://localhost:5000
```
**Status**: ✅ Configured  
**Works for**: Local development and Replit

## 🟡 OPTIONAL (App Works Without These)

### 1. WhatsApp Integration
```env
META_VERIFY_TOKEN=cybersathi_dev_token_2024
META_ACCESS_TOKEN=test_access_token
```
**Status**: ⚠️ Mock values (WhatsApp disabled)  
**Needed for**: WhatsApp chatbot functionality  
**App works without it**: Yes - just no WhatsApp features

### 2. Google Sign-In
```env
GOOGLE_CLIENT_ID=not_configured
GOOGLE_CLIENT_SECRET=not_configured
```
**Status**: ⚠️ Disabled  
**Needed for**: "Sign in with Google" button  
**App works without it**: Yes - use email/password signup instead

### 3. Redis & Celery
```env
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
```
**Status**: ⚠️ Not running (optional)  
**Needed for**: Background tasks, caching  
**App works without it**: Yes - core features work fine

### 4. NCRP Integration
```env
NCRP_MOCK_MODE=True
```
**Status**: ✅ Mock mode enabled  
**Needed for**: Submitting to National Cybercrime Portal  
**App works without it**: Yes - complaints save locally

### 5. SMS & Email Services
```env
SMS_API_KEY=not_configured
EMAIL_SERVICE_API_KEY=not_configured
```
**Status**: ⚠️ Disabled  
**Needed for**: SMS/Email notifications  
**App works without it**: Yes - no notifications sent

### 6. Sentry Error Tracking
```env
SENTRY_DSN=
```
**Status**: ⚠️ Disabled  
**Needed for**: Production error monitoring  
**App works without it**: Yes - check logs manually

## Configuration Priority

### For Local Development
1. ✅ MongoDB Atlas (REQUIRED)
2. ✅ Admin credentials (already set)
3. ✅ Security keys (already set)
4. Everything else: Optional

### For Testing WhatsApp Features
1. ✅ MongoDB Atlas
2. ✅ WhatsApp Meta Cloud API credentials
3. Everything else: Optional

### For Production Deployment
1. ✅ MongoDB Atlas (production cluster)
2. ✅ New SECRET_KEY & ENCRYPTION_KEY
3. ✅ Strong ADMIN_PASSWORD
4. ✅ CORS_ORIGINS (your frontend domain)
5. ✅ WhatsApp credentials (if using chatbot)
6. ✅ NCRP_MOCK_MODE=False (with real credentials)
7. Optional: Sentry, Redis, Email/SMS services

## How to Update .env

1. **Open the file**:
   ```bash
   backend/.env
   ```

2. **Find the setting** you want to change

3. **Edit the value** after the `=` sign:
   ```env
   # Before
   MONGODB_URL=mongodb://localhost:27017
   
   # After
   MONGODB_URL=mongodb+srv://myuser:mypass@cluster.mongodb.net/cybersathi
   ```

4. **Save the file**

5. **Restart the backend**:
   - In Replit: Click Stop → Play on backend workflow
   - In terminal: Press Ctrl+C and run `python -m uvicorn app.main:app --reload`

## Verification

### Check if MongoDB is Connected
Look for this in backend logs:
```
✅ MongoDB Atlas connected successfully
✅ Default admin created: admin@cybersathi.in
```

### Check if App is Ready
Look for this:
```
🌟 CyberSathi v1.0.0 is ready!
📊 API Docs: http://0.0.0.0:8000/docs
```

## Common Mistakes

❌ **Forgot to restart backend after editing .env**  
✅ Always restart to load new values

❌ **Password has special characters in MongoDB URL**  
✅ URL-encode special characters or use a simpler password

❌ **Copied connection string without database name**  
✅ Add `/cybersathi` before the `?` in the URL

❌ **Left `<password>` placeholder in MongoDB URL**  
✅ Replace with your actual password

## Need Help?

- **MongoDB Setup**: See [MONGODB_SETUP.md](MONGODB_SETUP.md)
- **Application Status**: See [CURRENT_STATUS.md](CURRENT_STATUS.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Production Checklist**: See [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)

## Summary

**Right Now**: Only MongoDB Atlas needs configuration  
**Everything Else**: Already set to reasonable defaults  
**Next Step**: [Set up MongoDB Atlas](MONGODB_SETUP.md) (5 minutes)
