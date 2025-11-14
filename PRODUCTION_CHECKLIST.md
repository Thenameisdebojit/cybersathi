# CyberSathi Production Deployment Checklist

## Pre-Deployment Checklist

### 1. MongoDB Atlas Setup
- [ ] Created MongoDB Atlas account
- [ ] Created free M0 cluster
- [ ] Created database user with strong password
- [ ] Configured network access (added deployment server IPs or 0.0.0.0/0 for testing)
- [ ] Obtained connection string
- [ ] Tested connection string from deployment environment

### 2. Environment Configuration

#### Backend Environment (.env.production)
- [ ] Set `DEBUG=False`
- [ ] Set `ENVIRONMENT=production`
- [ ] Generated NEW `SECRET_KEY` (32+ random characters)
- [ ] Generated NEW `ENCRYPTION_KEY` (32 bytes base64)
- [ ] Set strong `ADMIN_PASSWORD` (12+ characters, mixed case, numbers, symbols)
- [ ] Updated `MONGODB_URL` with Atlas connection string
- [ ] Updated `FRONTEND_URL` with production frontend domain
- [ ] Updated `CORS_ORIGINS` with production frontend domain only
- [ ] Configured WhatsApp API credentials (if using chatbot)
- [ ] Reviewed all secrets are unique and strong

#### Frontend Environment (.env.production)
- [ ] Set `VITE_API_URL` to backend URL (e.g., `https://api.cybersathi.com/api/v1`)

### 3. Backend Deployment

Choose ONE hosting option:

#### Option A: Render.com
- [ ] Created Render.com account
- [ ] Created new Web Service
- [ ] Connected GitHub repository
- [ ] Set build command: `pip install -r backend/requirements.txt`
- [ ] Set start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Added all environment variables from `.env.production`
- [ ] Deployment successful
- [ ] Health check passing: `https://your-api.onrender.com/health`

#### Option B: Railway.app
- [ ] Created Railway account
- [ ] New Project from GitHub
- [ ] Selected backend directory
- [ ] Added environment variables
- [ ] Deployment successful

#### Option C: Docker + Cloud Provider
- [ ] Built Docker image
- [ ] Pushed to container registry
- [ ] Deployed to cloud (AWS ECS / Google Cloud Run / DigitalOcean)
- [ ] Service running and accessible

### 4. Frontend Deployment (Vercel)
- [ ] Created Vercel account
- [ ] Connected GitHub repository
- [ ] Set root directory to `frontend`
- [ ] Set build command: `npm run build`
- [ ] Set output directory: `dist`
- [ ] Added `VITE_API_URL` environment variable
- [ ] Deployment successful
- [ ] Site accessible at production URL

### 5. DNS & Domain Configuration (Optional)
- [ ] Purchased domain name
- [ ] Configured DNS for frontend (Vercel)
- [ ] Configured DNS for backend (Render/Railway)
- [ ] SSL/TLS certificates auto-provisioned
- [ ] Both sites accessible via custom domains

### 6. Security Verification
- [ ] API only accepts requests from allowed origins (CORS)
- [ ] All secrets are unique and not from examples
- [ ] Admin password is strong and documented securely
- [ ] MongoDB network access is properly restricted
- [ ] API docs disabled in production (`/docs` returns 404)
- [ ] No sensitive data logged in production

### 7. Functional Testing
- [ ] Frontend loads successfully
- [ ] Can access login page
- [ ] Can sign up new user
- [ ] Can login with admin credentials from .env
- [ ] Dashboard displays after login
- [ ] API health endpoint works: `{backend_url}/health`
- [ ] Database connection confirmed (check backend logs)
- [ ] Logout works correctly

### 8. WhatsApp Integration (If Applicable)
- [ ] WhatsApp Business API configured
- [ ] Webhook URL set to `{backend_url}/webhook/whatsapp`
- [ ] Webhook verification successful
- [ ] Test message flow works end-to-end
- [ ] Complaint creation and ticket generation tested

### 9. Monitoring & Backup
- [ ] MongoDB Atlas backup enabled (automatic with Atlas)
- [ ] Error tracking configured (optional: Sentry)
- [ ] Uptime monitoring set up (optional: UptimeRobot, Pingdom)
- [ ] Log aggregation configured (check hosting platform logs)

### 10. Documentation
- [ ] Production URLs documented and shared with team
- [ ] Admin credentials stored in secure password manager
- [ ] MongoDB Atlas credentials stored securely
- [ ] API keys and secrets documented (not in code)
- [ ] Incident response plan documented

## Post-Deployment

### Immediate Actions
1. **Test Complete User Flow**:
   - New user signup
   - Login
   - Submit test complaint (if WhatsApp integrated)
   - View complaint in dashboard
   - Logout

2. **Create Test Data** (Optional):
   - Create additional admin users
   - Submit sample complaints for demo
   - Test all dashboard features

3. **Monitor for 24 Hours**:
   - Check error logs regularly
   - Monitor database connections
   - Watch for failed requests
   - Verify WhatsApp webhook receiving messages

### Week 1 Tasks
- [ ] Train admin users on the system
- [ ] Document common issues and solutions
- [ ] Set up regular backup verification
- [ ] Plan capacity monitoring

## Emergency Rollback Plan

If critical issues occur:

1. **Frontend Issues**:
   ```bash
   # Revert to previous Vercel deployment
   vercel rollback
   ```

2. **Backend Issues**:
   - Render/Railway: Use dashboard to rollback to previous deployment
   - Check logs for errors: View in hosting platform dashboard

3. **Database Issues**:
   - MongoDB Atlas: Restore from automatic backup
   - Point-in-time recovery available

## Support Contacts

- **Technical Issues**: [Your IT Team Contact]
- **MongoDB Atlas Support**: https://support.mongodb.com
- **Hosting Support**: 
  - Render: support@render.com
  - Railway: team@railway.app
- **WhatsApp API Support**: Meta Business Help Center

## Useful Commands

### Check Backend Health
```bash
curl https://your-backend-url.com/health
```

### View Backend Logs
- Render: `render logs`
- Railway: Check dashboard

### Test MongoDB Connection
```bash
mongosh "mongodb+srv://your-connection-string"
```

## Success Criteria

✅ All items in Pre-Deployment Checklist completed
✅ All items in Functional Testing passed
✅ Production URLs accessible and working
✅ No critical errors in logs for 24 hours
✅ Team trained and has access
✅ Backup and monitoring confirmed

---

**Date Deployed**: __________________
**Deployed By**: __________________
**Production URLs**:
- Frontend: __________________
- Backend API: __________________
- MongoDB Cluster: __________________
