# CyberSathi Deployment Guide

## Vercel Deployment (Recommended)

CyberSathi uses a **two-project deployment** architecture on Vercel:
1. **Frontend Project**: React Vite static site (uses `frontend/vercel.json`)
2. **Backend Project**: FastAPI Python serverless functions (uses `backend/vercel.json`)

### Prerequisites

- Vercel account (free tier works)
- MongoDB Atlas database (already configured)
- Git repository with this codebase

### Configuration Files
- `backend/vercel.json` - Backend deployment config (automatically detected when root = `backend/`)
- `frontend/vercel.json` - Frontend deployment config (automatically detected when root = `frontend/`)

**Note**: All sensitive environment variables (MongoDB URL, API keys, secrets) are configured via the Vercel dashboard, NOT in these config files.

---

## Step 1: Deploy Backend

### 1.1 Create Backend Vercel Project

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New Project"**
3. Import your Git repository
4. **Important**: Set **Root Directory** to `backend/`
5. Select **Framework Preset**: "Other"
6. **Note**: The `backend/vercel.json` file will be automatically detected
7. Click **"Deploy"** (will fail initially - we'll add env vars next)

### 1.2 Configure Backend Environment Variables

**IMPORTANT**: All environment variables must be added via the **Vercel Project Settings** → **Environment Variables** section. Do NOT commit secrets to Git.

In the Vercel project settings, add these environment variables:

| Variable | Value | Description | Required? |
|----------|-------|-------------|-----------|
| `MONGODB_URL` | `mongodb+srv://...` | Your MongoDB Atlas connection string | ✅ Yes |
| `SECRET_KEY` | Generate random string | JWT secret key (use: `openssl rand -hex 32`) | ✅ Yes |
| `FRONTEND_URL` | `https://your-frontend.vercel.app` | Your frontend URL (add after deploying frontend) | ✅ Yes |
| `CORS_ORIGINS_STR` | `https://your-frontend.vercel.app` | Same as FRONTEND_URL | ✅ Yes |
| `ADMIN_EMAIL` | `admin@cybersathi.in` | Admin user email | ✅ Yes |
| `ADMIN_PASSWORD` | Choose secure password | Admin user password | ✅ Yes |
| `OPENAI_API_KEY` | Your OpenAI key | For AI chatbot features | ⚠️ Optional |

**Note**: Copy the backend deployment URL (e.g., `https://cybersathi-backend.vercel.app`) - you'll need it for frontend configuration.

---

## Step 2: Deploy Frontend

### 2.1 Create Frontend Vercel Project

1. In Vercel Dashboard, click **"Add New Project"** again
2. Import the **same Git repository**
3. **Important**: Set **Root Directory** to `frontend/`
4. Select **Framework Preset**: "Vite"
5. **DO NOT deploy yet** - configure environment first

### 2.2 Configure Frontend Environment Variables

**IMPORTANT**: Add this via **Vercel Project Settings** → **Environment Variables**.

| Variable | Value | Description | Required? |
|----------|-------|-------------|-----------|
| `VITE_API_URL` | `https://your-backend.vercel.app/api/v1` | Backend API URL from Step 1.2 | ✅ Yes |

**Note**: The `frontend/vercel.json` file will be automatically detected by Vercel.

### 2.3 Deploy Frontend

1. Click **"Deploy"**
2. Wait for deployment to complete
3. Copy the frontend URL (e.g., `https://cybersathi.vercel.app`)

---

## Step 3: Update Backend CORS

1. Go back to your **backend Vercel project**
2. Update these environment variables with your actual frontend URL:
   - `FRONTEND_URL` = `https://cybersathi.vercel.app`
   - `CORS_ORIGINS_STR` = `https://cybersathi.vercel.app`
3. Trigger a redeployment (Settings → Redeploy)

---

## Step 4: Verify Deployment

### Backend Health Check
Visit: `https://your-backend.vercel.app/health`

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

### Frontend Check
Visit: `https://your-frontend.vercel.app`

You should see:
- CyberSathi home page with logo
- "Sign In" and "Get Started" buttons
- No console errors

### Test Authentication
1. Click "Get Started"
2. Create a new account
3. Log in successfully
4. Access dashboard

---

## Environment Variables Summary

### Backend (7 required + 1 optional)
```
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/cybersathi
SECRET_KEY=your-random-secret-key-here
FRONTEND_URL=https://cybersathi.vercel.app
CORS_ORIGINS_STR=https://cybersathi.vercel.app
ADMIN_EMAIL=admin@cybersathi.in
ADMIN_PASSWORD=your-secure-admin-password
OPENAI_API_KEY=sk-... (optional)
```

### Frontend (1 required)
```
VITE_API_URL=https://cybersathi-backend.vercel.app/api/v1
```

---

## Local Development

### Backend
```bash
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd frontend
npm run dev
```

The frontend will run on `http://localhost:5000` and connect to the backend on `http://localhost:8000`.

---

## Troubleshooting

### Backend Deployment Fails
- Check that Root Directory is set to `backend/`
- Verify all environment variables are set correctly
- Check MongoDB Atlas IP whitelist (allow `0.0.0.0/0` for Vercel)

### Frontend Can't Connect to Backend
- Verify `VITE_API_URL` is set correctly
- Check backend CORS settings (`CORS_ORIGINS_STR`)
- Open browser console to see API errors

### MongoDB Connection Issues
- Ensure MongoDB Atlas allows connections from anywhere (Vercel uses dynamic IPs)
- Verify connection string is correct
- Check database user permissions

### CORS Errors
- Update `CORS_ORIGINS_STR` in backend with your actual frontend URL
- Redeploy backend after updating CORS settings

---

## Production Checklist

- [ ] Backend deployed and health check passes
- [ ] Frontend deployed and loads correctly
- [ ] MongoDB Atlas configured with correct credentials
- [ ] All environment variables set in Vercel
- [ ] CORS configured with actual frontend URL
- [ ] Admin account accessible
- [ ] User registration works
- [ ] User login works
- [ ] Dashboard accessible after login
- [ ] WhatsApp webhook configured (if using)
- [ ] SSL/HTTPS working (automatic on Vercel)

---

## Custom Domain (Optional)

### Backend
1. Go to backend Vercel project → Settings → Domains
2. Add custom domain (e.g., `api.cybersathi.com`)
3. Configure DNS as instructed
4. Update `VITE_API_URL` in frontend to use new domain

### Frontend
1. Go to frontend Vercel project → Settings → Domains
2. Add custom domain (e.g., `cybersathi.com`)
3. Configure DNS as instructed
4. Update `CORS_ORIGINS_STR` in backend to use new domain

---

## Security Notes

- **Never commit** environment variables to Git
- Use Vercel's encrypted environment variables
- Rotate `SECRET_KEY` periodically
- Use strong `ADMIN_PASSWORD`
- Keep `MONGODB_URL` secure
- Enable MongoDB Atlas IP whitelist for production
- Configure firewall rules as needed

---

## Support

For deployment issues:
- Check Vercel deployment logs
- Review MongoDB Atlas logs
- Check browser console for errors
- Verify all environment variables

For feature issues:
- Check backend API docs: `https://your-backend.vercel.app/docs`
- Review application logs in Vercel dashboard
