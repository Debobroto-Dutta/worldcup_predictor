# Deploy Latest Files to Render

## 🚀 Step-by-Step Deployment Guide

### Step 1: Commit Your Changes to Git

```bash
# Navigate to your project
cd worldcup-predictor

# Check what files changed
git status

# Add all changed files
git add .

# Commit with a message
git commit -m "Add live football scores integration"

# Push to GitHub
git push origin main
```

**Note:** Replace `main` with `master` if that's your default branch.

### Step 2: Deploy to Render

Render will automatically deploy if you have auto-deploy enabled. If not:

#### Option A: Automatic Deploy (If Enabled)
- Just push to GitHub
- Render detects the changes
- Automatically deploys
- Wait 2-5 minutes

#### Option B: Manual Deploy
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click on your service
3. Click **"Manual Deploy"** button
4. Select **"Deploy latest commit"**
5. Click **"Deploy"**

### Step 3: Monitor Deployment

Watch the deployment logs in Render:
1. Go to your service in Render Dashboard
2. Click on **"Logs"** tab
3. Watch for:
   ```
   ==> Building...
   ==> Deploying...
   ==> Starting service...
   ✓ Database tables checked/created
   ✓ Backfilled X historical match result(s)
   ✓ Match result auto-updater started
   ```

### Step 4: Test Your Deployed App

Once deployment is complete:

```bash
# Replace with your actual Render URL
export APP_URL="https://your-app-name.onrender.com"

# Test live scores endpoint
curl $APP_URL/api/live-scores

# Test matches endpoint
curl $APP_URL/api/matches

# Test teams endpoint
curl $APP_URL/api/teams
```

## 📋 Complete Deployment Checklist

### Before Pushing to GitHub:

```bash
# 1. Make sure you're in the right directory
cd worldcup-predictor

# 2. Check git status
git status

# 3. Review changes
git diff

# 4. Add all files
git add .

# 5. Commit
git commit -m "Add live football scores integration with worldcupjson.net API"

# 6. Push to GitHub
git push origin main
```

### Files That Were Modified/Created:

- ✅ `backend/match_updater.py` - Enhanced with team mapping and new methods
- ✅ `backend/app.py` - Added new API endpoints
- ✅ `backend/sync_matches.py` - New sync utility script
- ✅ `README.md` - Updated with new features
- ✅ `LIVE_SCORES_GUIDE.md` - Complete integration guide
- ✅ `QUICK_START_LIVE_SCORES.md` - Quick start guide
- ✅ `HOW_TO_SYNC_DATABASE.md` - Database sync guide
- ✅ `SYNC_ON_RENDER.md` - Render-specific guide
- ✅ `DEPLOY_TO_RENDER.md` - This deployment guide

### After Deployment on Render:

1. **Check Logs**
   - Look for successful startup messages
   - Verify backfill completed
   - Confirm scheduler started

2. **Test Endpoints**
   ```bash
   curl https://your-app-name.onrender.com/api/matches
   curl https://your-app-name.onrender.com/api/live-scores
   curl https://your-app-name.onrender.com/api/teams
   ```

3. **Login and Test Admin Panel**
   - Go to your app URL
   - Login as admin
   - Check if "Sync Matches" button works
   - Verify matches are displayed

## 🔧 Troubleshooting Deployment

### Git Push Issues

**Error: "fatal: not a git repository"**
```bash
# Initialize git if needed
git init
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git add .
git commit -m "Initial commit with live scores"
git push -u origin main
```

**Error: "Updates were rejected"**
```bash
# Pull first, then push
git pull origin main --rebase
git push origin main
```

### Render Deployment Issues

**Build Failed**
- Check Render logs for error messages
- Verify `requirements.txt` is correct
- Make sure all dependencies are listed

**App Crashes on Startup**
- Check Render logs
- Look for Python errors
- Verify environment variables are set

**Database Connection Issues**
- Render should auto-configure PostgreSQL
- Check if DATABASE_URL is set in environment variables

## 🎯 Quick Commands Reference

### Git Commands
```bash
# Check status
git status

# Add all files
git add .

# Commit
git commit -m "Your message here"

# Push to GitHub
git push origin main

# Check remote
git remote -v

# View commit history
git log --oneline
```

### Test Deployed App
```bash
# Set your app URL
export APP_URL="https://your-app-name.onrender.com"

# Test endpoints
curl $APP_URL/api/health
curl $APP_URL/api/matches
curl $APP_URL/api/live-scores
curl $APP_URL/api/teams
curl $APP_URL/api/leaderboard
```

## 📊 Verify Everything Works

### 1. Check Render Dashboard
- ✅ Service status: "Live"
- ✅ Latest deploy: Successful
- ✅ Logs show no errors

### 2. Test Public Endpoints
```bash
# Should return live matches (if any)
curl https://your-app-name.onrender.com/api/live-scores

# Should return 64 matches
curl https://your-app-name.onrender.com/api/matches | grep -o "id" | wc -l

# Should return teams data
curl https://your-app-name.onrender.com/api/teams
```

### 3. Test Web Interface
1. Open: `https://your-app-name.onrender.com`
2. Register/Login
3. Check if matches are displayed
4. Make a prediction
5. Check leaderboard

### 4. Test Admin Functions
1. Login as admin
2. Go to Admin Panel
3. Click "Sync Matches" - should work
4. Click "Backfill Results" - should work
5. Check "Test API" - should show 64 matches

## ✅ Success Indicators

You'll know it's working when:

### In Render Logs:
```
✓ Database tables checked/created
✓ Backfilled 48 historical match result(s)
✓ Automatic match result updater initialized
✓ Match result auto-updater started (runs every 15 minutes)
```

### In Your Browser:
- App loads without errors
- Matches are displayed
- Predictions can be made
- Leaderboard shows rankings
- Admin panel works

### Via API:
```bash
curl https://your-app-name.onrender.com/api/matches
# Returns JSON with 64 matches
```

## 🎉 You're Done!

Your app is now deployed with live football scores! 🚀⚽

### What Happens Next:
- ✅ Scores update automatically every 15 minutes
- ✅ Points are calculated when matches finish
- ✅ Leaderboard updates in real-time
- ✅ No manual intervention needed

## 📱 Share Your App

Your app is live at:
```
https://your-app-name.onrender.com
```

Share this URL with your friends to start predicting!

---

**Need help?** Check:
- Render logs for errors
- `SYNC_ON_RENDER.md` for Render-specific help
- `LIVE_SCORES_GUIDE.md` for API documentation