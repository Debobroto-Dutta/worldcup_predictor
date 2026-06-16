# How to Sync Database on Render

## 🌐 Your App is Deployed on Render

Good news! The live scores integration works automatically on Render. Here's how to sync your database.

## 🚀 Method 1: Automatic Sync (Easiest - Already Working!)

**Your app syncs automatically when it starts on Render!**

When Render deploys your app, it:
1. ✅ Starts the Flask app
2. ✅ Automatically backfills all historical match results
3. ✅ Starts the scheduler (updates every 15 minutes)
4. ✅ Keeps updating scores automatically

**You don't need to do anything!** Just deploy and it works.

### Check Render Logs

Go to your Render dashboard → Your service → Logs

You should see:
```
✓ Database tables checked/created
✓ Backfilled 48 historical match result(s)
✓ Automatic match result updater initialized
✓ Match result auto-updater started (runs every 15 minutes)
```

## 🔧 Method 2: Manual Sync via Admin Panel

### Step 1: Access your deployed app
```
https://your-app-name.onrender.com
```

### Step 2: Login as admin
1. Go to your app URL
2. Login with admin credentials
3. Navigate to Admin Panel

### Step 3: Click "Sync Matches"
- This will sync all 64 matches from the API
- Updates existing matches with scores
- Shows success message

### Step 4: Click "Backfill Results" (optional)
- Updates all historical match results
- Recalculates all prediction points

## 🌐 Method 3: Using API Endpoints

### Sync Matches
```bash
curl -X POST https://your-app-name.onrender.com/api/admin/sync-matches \
  -H "Content-Type: application/json" \
  --cookie "session=YOUR_SESSION_COOKIE"
```

### Backfill Results
```bash
curl -X POST https://your-app-name.onrender.com/api/admin/backfill-results \
  -H "Content-Type: application/json" \
  --cookie "session=YOUR_SESSION_COOKIE"
```

### Test API Connection
```bash
curl https://your-app-name.onrender.com/api/admin/test-api \
  --cookie "session=YOUR_SESSION_COOKIE"
```

## 📊 Verify It's Working

### Check Live Scores (Public Endpoint)
```bash
curl https://your-app-name.onrender.com/api/live-scores
```

### Check All Matches (Public Endpoint)
```bash
curl https://your-app-name.onrender.com/api/matches
```

### Check Teams (Public Endpoint)
```bash
curl https://your-app-name.onrender.com/api/teams
```

## 🔄 How Automatic Updates Work on Render

### Background Scheduler
Your app runs a background scheduler that:
- ✅ Checks for finished matches every 15 minutes
- ✅ Updates scores automatically
- ✅ Calculates prediction points
- ✅ Runs 24/7 on Render

### What Gets Updated Automatically
1. Match scores (when matches finish)
2. Match status (completed, in_progress, etc.)
3. Prediction points (calculated automatically)
4. Leaderboard rankings (updated in real-time)

## 🚨 Important Notes for Render

### 1. Database Persistence
- ✅ Render uses PostgreSQL (persistent)
- ✅ Data is saved permanently
- ✅ Survives app restarts

### 2. Scheduler Runs Continuously
- ✅ Background scheduler keeps running
- ✅ Updates every 15 minutes
- ✅ No manual intervention needed

### 3. Free Tier Considerations
If you're on Render's free tier:
- App may sleep after 15 minutes of inactivity
- Scheduler stops when app sleeps
- Wakes up on next request
- Consider upgrading for 24/7 updates

## 🔍 Troubleshooting on Render

### Check Logs
```
Render Dashboard → Your Service → Logs
```

Look for:
- ✅ "Backfilled X historical match result(s)"
- ✅ "Match result auto-updater started"
- ✅ "Updated: Team A X-Y Team B"

### No Matches in Database?

**Option 1: Redeploy**
```
Render Dashboard → Your Service → Manual Deploy
```

**Option 2: Use Admin Panel**
1. Login to your app
2. Go to Admin Panel
3. Click "Sync Matches"

### Scores Not Updating?

**Check if scheduler is running:**
1. Look at Render logs
2. Should see periodic update messages
3. If not, redeploy the app

**Manual trigger:**
1. Login as admin
2. Click "Backfill Results"

## 📝 Deployment Checklist

When deploying to Render, make sure:
- [x] `requirements.txt` includes all dependencies
- [x] `APScheduler==3.10.4` is in requirements.txt
- [x] `requests==2.31.0` is in requirements.txt
- [x] Environment variables are set (if any)
- [x] Database is PostgreSQL (not SQLite)

## 🎯 Quick Commands for Render

### Get Session Cookie (for API calls)
1. Open your app in browser
2. Login as admin
3. Press F12 (Developer Tools)
4. Go to Application → Cookies
5. Copy the `session` cookie value

### Test from Command Line
```bash
# Replace YOUR_APP_NAME and YOUR_SESSION_COOKIE
export APP_URL="https://your-app-name.onrender.com"
export SESSION="your_session_cookie_here"

# Test API
curl "$APP_URL/api/admin/test-api" --cookie "session=$SESSION"

# Sync matches
curl -X POST "$APP_URL/api/admin/sync-matches" --cookie "session=$SESSION"

# Get live scores (no auth needed)
curl "$APP_URL/api/live-scores"
```

## ✅ Success Indicators

Your sync is working if you see:

### In Render Logs:
```
✓ Database tables checked/created
✓ Backfilled 48 historical match result(s)
✓ Match result auto-updater started (runs every 15 minutes)
✅ Updated: England 2-1 France
```

### In Your App:
- Matches show up on the frontend
- Finished matches have scores
- Leaderboard shows points
- Admin panel shows all matches

### Via API:
```bash
curl https://your-app-name.onrender.com/api/matches
# Should return 64 matches
```

## 🎉 That's It!

Your app on Render now:
- ✅ Syncs automatically on startup
- ✅ Updates scores every 15 minutes
- ✅ Calculates points automatically
- ✅ Works 24/7 (on paid plans)

**No manual sync needed!** Just deploy and it works.

---

**Need help?** Check:
- Render logs for errors
- `HOW_TO_SYNC_DATABASE.md` for local testing
- `LIVE_SCORES_GUIDE.md` for full documentation