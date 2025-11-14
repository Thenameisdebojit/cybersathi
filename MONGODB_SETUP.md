# MongoDB Atlas Quick Setup Guide

## Get Your App Running in 5 Minutes!

Your CyberSathi app needs MongoDB to work. Follow these simple steps:

### Step 1: Create Free MongoDB Atlas Account

1. Go to https://www.mongodb.com/cloud/atlas/register
2. Sign up with email (FREE forever for development)
3. Verify your email

### Step 2: Create a FREE Cluster

1. After login, click **"Build a Database"**
2. Choose **"M0 FREE"** tier (no credit card needed!)
3. Select a cloud provider (AWS recommended) and region closest to you
4. Click **"Create Cluster"** (takes 3-5 minutes to provision)

### Step 3: Configure Database Access

1. On the left sidebar, click **"Database Access"**
2. Click **"Add New Database User"**
3. Create credentials:
   - Username: `cybersathi_admin`
   - Password: Click "Autogenerate Secure Password" and **COPY IT**
   - Select "Read and write to any database"
4. Click **"Add User"**

### Step 4: Configure Network Access

1. On the left sidebar, click **"Network Access"**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (for development)
4. Click **"Confirm"**

### Step 5: Get Connection String

1. Go back to **"Database"** in left sidebar
2. Click **"Connect"** button on your cluster
3. Choose **"Connect your application"**
4. Copy the connection string - looks like:
   ```
   mongodb+srv://cybersathi_admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. **IMPORTANT**: Replace `<password>` with the password you copied earlier!

### Step 6: Update Your Backend .env File

Open `backend/.env` and update this line:

```env
MONGODB_URL=mongodb+srv://cybersathi_admin:YOUR_ACTUAL_PASSWORD@cluster0.xxxxx.mongodb.net/cybersathi?retryWrites=true&w=majority
```

**Make sure to**:
- Replace `YOUR_ACTUAL_PASSWORD` with your actual password
- Add `/cybersathi` before the `?` (this is your database name)

### Step 7: Restart Backend

In Replit:
1. Stop the backend workflow (click stop button)
2. Start it again (click play button)

You should see:
```
✅ MongoDB Atlas connected successfully
✅ Default admin created
```

## Troubleshooting

### "Authentication failed"
- Double-check your password in the connection string
- Make sure there are no spaces in the password section

### "Connection refused"
- Make sure you clicked "Allow Access from Anywhere" in Network Access
- Wait 2-3 minutes for network settings to propagate

### "Timeout"
- Check your internet connection
- Verify the cluster is active (green checkmark in Atlas dashboard)

## You're Done!

Now your app will have:
- ✅ Working login/signup
- ✅ User authentication
- ✅ Complaint storage
- ✅ Full database functionality

## Free Tier Limits

MongoDB Atlas M0 (Free) gives you:
- 512 MB storage (plenty for development!)
- Shared RAM and vCPU
- No credit card required
- Perfect for testing and small projects
