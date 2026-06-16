# 🚀 Quick Deployment Commands

## Deploy to Render in 3 Steps

### Step 1: Commit to Git
```bash
cd worldcup-predictor
git add .
git commit -m "Add live football scores integration"
git push origin main
```

### Step 2: Deploy on Render
- Go to [Render Dashboard](https://dashboard.render.com/)
- Click your service → **"Manual Deploy"** → **"Deploy latest commit"**

### Step 3: Test
```bash
# Replace with your Render URL
curl https://your-app-name.onrender.com/api/matches
curl https://your-app-name.onrender.com/api/live-scores
```

## ✅ That's It!

Your app now has:
- ✅ Live football scores (updates every 15 minutes)
- ✅ 64 World Cup matches synced automatically
- ✅ Automatic points calculation
- ✅ Admin panel with sync controls

## 📚 Full Guides Available

- **`DEPLOY_TO_RENDER.md`** - Complete deployment guide
- **`SYNC_ON_RENDER.md`** - How syncing works on Render
- **`LIVE_SCORES_GUIDE.md`** - Full API documentation
- **`QUICK_START_LIVE_SCORES.md`** - Quick start guide

---

**Questions?** Check the guides above or Render logs for details.