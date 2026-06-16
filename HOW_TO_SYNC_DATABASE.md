# How to Sync Your Database with Live Scores

## 📋 Prerequisites

Make sure you have:
1. Python 3.8+ installed
2. Your virtual environment activated
3. All dependencies installed

## 🚀 Method 1: Using the Sync Script (Easiest)

### Step 1: Navigate to your project
```bash
cd worldcup-predictor
```

### Step 2: Activate virtual environment

**On Linux/Mac:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### Step 3: Install dependencies (if not already done)
```bash
pip install -r requirements.txt
```

### Step 4: Run the sync script
```bash
python3 backend/sync_matches.py
```

**What this does:**
- ✅ Tests API connection
- ✅ Fetches all 64 matches from worldcupjson.net
- ✅ Fetches all 32 teams
- ✅ Creates matches in your database
- ✅ Updates existing matches with scores
- ✅ Shows you a summary

**Expected Output:**
```
============================================================
World Cup Match Sync Utility
============================================================

1. Testing API connection...
✅ Connected! Found 64 matches from API

2. Fetching teams...
✅ Found 32 teams in 8 groups

3. Syncing matches to database...
✅ Created: Qatar vs Ecuador
✅ Created: England vs Iran
...

============================================================
SYNC SUMMARY
============================================================
Matches created: 64
Matches updated: 0
Total matches in API: 64

✅ Sync complete!
```

## 🌐 Method 2: Using the Web Interface (Admin Panel)

### Step 1: Start your Flask app
```bash
python3 -m backend.app
```

### Step 2: Login as admin
1. Open browser: http://localhost:5000
2. Login with admin credentials
3. Go to Admin Panel

### Step 3: Click "Sync Matches" button
- This will sync all matches from the API
- You'll see a success message with counts

## 🔧 Method 3: Using API Endpoint (Advanced)

### Step 1: Start your app
```bash
python3 -m backend.app
```

### Step 2: Get your session cookie
1. Login via browser
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies
4. Copy the session cookie value

### Step 3: Call the sync endpoint
```bash
curl -X POST http://localhost:5000/api/admin/sync-matches \
  -H "Content-Type: application/json" \
  --cookie "session=YOUR_SESSION_COOKIE_HERE"
```

**Response:**
```json
{
  "message": "Sync complete: 64 created, 0 updated",
  "created_count": 64,
  "updated_count": 0
}
```

## 🔄 Method 4: Automatic Sync (Recommended for Production)

Your app automatically syncs when it starts!

### Step 1: Just start your app
```bash
python3 -m backend.app
```

**What happens automatically:**
1. ✅ Database tables are created/checked
2. ✅ Historical results are backfilled
3. ✅ Scheduler starts (updates every 15 minutes)
4. ✅ Finished matches get scores automatically

**You'll see:**
```
✓ Database tables checked/created
✓ Backfilled 48 historical match result(s)
✓ Automatic match result updater initialized
✓ Match result auto-updater started (runs every 15 minutes)
```

## 📊 Verify the Sync Worked

### Check via API:
```bash
curl http://localhost:5000/api/matches | python3 -m json.tool
```

### Check via Database (SQLite):
```bash
sqlite3 instance/worldcup.db "SELECT COUNT(*) FROM match;"
```

Should show 64 matches.

### Check specific match:
```bash
sqlite3 instance/worldcup.db "SELECT team_home, team_away, home_score, away_score, is_finished FROM match LIMIT 5;"
```

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'flask'"

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Error: "No module named 'backend'"

**Solution:** Run from the worldcup-predictor directory
```bash
cd worldcup-predictor
python3 backend/sync_matches.py
```

### No matches created?

**Check API connection:**
```bash
curl https://worldcupjson.net/matches
```

If this works, the API is fine. Try running sync again.

### Matches not updating scores?

**Manual backfill:**
```bash
# Start Python in your project directory
python3
```

```python
from backend.app import app
from backend.match_updater import MatchUpdater

updater = MatchUpdater(app)
updated = updater.backfill_all_results()
print(f"Updated {updated} matches")
```

## 📝 What Gets Synced?

From the API, you get:
- ✅ All 64 World Cup matches
- ✅ Team names (Qatar, Ecuador, England, etc.)
- ✅ Match dates and times
- ✅ Match stages (Group Stage, Round of 16, etc.)
- ✅ Scores (for finished matches)
- ✅ Match status (completed, in_progress, etc.)

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Sync all matches | `python3 backend/sync_matches.py` |
| Start app (auto-sync) | `python3 -m backend.app` |
| Check matches | `curl http://localhost:5000/api/matches` |
| Get live scores | `curl http://localhost:5000/api/live-scores` |
| Manual backfill | Use admin panel or API endpoint |

## ✅ Success Checklist

After syncing, you should have:
- [ ] 64 matches in database
- [ ] All team names matching API (Qatar, England, Brazil, etc.)
- [ ] Finished matches have scores
- [ ] App shows matches on frontend
- [ ] Automatic updates running every 15 minutes

---

**Need more help?** Check:
- `QUICK_START_LIVE_SCORES.md` - Quick start guide
- `LIVE_SCORES_GUIDE.md` - Full documentation