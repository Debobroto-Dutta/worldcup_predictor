# 🔧 Fix Your App - Update Match Scores

## Your App: https://worldcup-predictor.onrender.com

## 🚀 Quick Fix (Choose One)

### Option 1: Use Admin Panel (EASIEST) ⭐

1. Go to: **https://worldcup-predictor.onrender.com**
2. Login as admin
3. Click **"Backfill Results"** button in admin panel
4. ✅ Done! All matches will be updated

### Option 2: Use API Endpoint

```bash
# First, get your session cookie:
# 1. Login to https://worldcup-predictor.onrender.com
# 2. Press F12 → Application → Cookies
# 3. Copy the 'session' cookie value

# Then run:
curl -X POST https://worldcup-predictor.onrender.com/api/admin/backfill-results \
  -H "Content-Type: application/json" \
  --cookie "session=YOUR_SESSION_COOKIE_HERE"
```

### Option 3: Redeploy on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Find "worldcup-predictor" service
3. Click **"Manual Deploy"**
4. Select **"Deploy latest commit"**
5. Wait 2-5 minutes
6. ✅ App will auto-fix on startup!

## 📊 Test It Worked

### Check matches are updated:
```bash
curl https://worldcup-predictor.onrender.com/api/matches | grep -o '"is_finished":true' | wc -l
```

Should show ~48 finished matches.

### Check specific match:
```bash
curl https://worldcup-predictor.onrender.com/api/matches | python3 -m json.tool | head -30
```

Should see scores like:
```json
{
  "id": 1,
  "team_home": "Qatar",
  "team_away": "Ecuador",
  "home_score": 0,
  "away_score": 2,
  "is_finished": true
}
```

### Check live scores endpoint:
```bash
curl https://worldcup-predictor.onrender.com/api/live-scores
```

### Check teams:
```bash
curl https://worldcup-predictor.onrender.com/api/teams
```

## ✅ What Should Happen

After the fix:
- ✅ ~48 matches marked as "finished"
- ✅ All finished matches show scores (e.g., Qatar 0-2 Ecuador)
- ✅ Matches no longer show "in progress" incorrectly
- ✅ Prediction points calculated automatically
- ✅ Leaderboard updated with correct points

## 🔍 Check Render Logs

Go to: Render Dashboard → worldcup-predictor → Logs

Look for:
```
✓ Backfilled 48 historical match result(s)
✅ Updated: Qatar 0-2 Ecuador
✅ Updated: England 6-2 Iran
...
```

## 🎯 Recommended: Use Admin Panel

**Easiest way:**
1. Visit: https://worldcup-predictor.onrender.com
2. Login as admin
3. Go to Admin Panel
4. Click "Backfill Results"
5. See success message
6. Refresh page - matches updated! ✅

## 📝 Deploy Latest Changes

To deploy all the new live score features:

```bash
cd worldcup-predictor
git add .
git commit -m "Add live football scores integration"
git push origin main
```

Then on Render:
- Dashboard → worldcup-predictor → Manual Deploy

## 🆘 Still Not Working?

### Check Team Names

Your database team names MUST match the API exactly:
- Qatar, Ecuador, Senegal, Netherlands
- England, Iran, United States, Wales
- Argentina, Saudi Arabia, Mexico, Poland
- etc.

If they don't match, the updater can't find them!

### Manual Check

```bash
# Check what's in your database
curl https://worldcup-predictor.onrender.com/api/matches | python3 -m json.tool | grep team_home

# Compare with API
curl https://worldcupjson.net/matches | python3 -m json.tool | grep '"name"'
```

Team names must be identical!

---

**Quick Summary:**
1. Login to https://worldcup-predictor.onrender.com as admin
2. Click "Backfill Results"
3. Done! ✅