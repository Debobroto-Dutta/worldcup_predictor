# 🔧 Fix Matches - Update Scores Now

## Problem
Your matches show "in progress" but they're actually finished. You need to update them with scores from the API.

## 🚀 Quick Fix (3 Options)

### Option 1: Run Fix Script (Easiest)

```bash
cd worldcup-predictor
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

python3 backend/fix_matches.py
```

This will:
- ✅ Fetch all matches from API
- ✅ Update finished matches with scores
- ✅ Mark them as completed
- ✅ Calculate prediction points

### Option 2: Use Admin Panel (On Render)

1. Go to your app: `https://your-app-name.onrender.com`
2. Login as admin
3. Click **"Backfill Results"** button
4. Wait for success message

### Option 3: Use API Endpoint

```bash
# Get your session cookie first (login via browser, F12 → Application → Cookies)
curl -X POST https://your-app-name.onrender.com/api/admin/backfill-results \
  -H "Content-Type: application/json" \
  --cookie "session=YOUR_SESSION_COOKIE"
```

## 📊 Verify It Worked

### Check via API:
```bash
curl https://your-app-name.onrender.com/api/matches | grep -o '"is_finished":true' | wc -l
```

Should show ~48 finished matches.

### Check specific match:
```bash
curl https://your-app-name.onrender.com/api/matches | python3 -m json.tool | grep -A 5 "Qatar"
```

Should show scores like:
```json
{
  "team_home": "Qatar",
  "team_away": "Ecuador",
  "home_score": 0,
  "away_score": 2,
  "is_finished": true
}
```

## 🐛 If It Still Doesn't Work

### Check Team Names Match

The API uses these exact names:
- Qatar, Ecuador, Senegal, Netherlands
- England, Iran, United States, Wales
- Argentina, Saudi Arabia, Mexico, Poland
- France, Australia, Denmark, Tunisia
- Spain, Costa Rica, Germany, Japan
- Belgium, Canada, Morocco, Croatia
- Brazil, Serbia, Switzerland, Cameroon
- Portugal, Ghana, Uruguay, South Korea

**Your database must use these EXACT names!**

### Update Team Names in Database

If your team names don't match, update them:

```python
# Run Python in your project directory
python3

from backend.app import app
from backend.models import db, Match

with app.app_context():
    # Example: Update "USA" to "United States"
    matches = Match.query.filter(
        db.or_(
            Match.team_home.like('%USA%'),
            Match.team_away.like('%USA%')
        )
    ).all()
    
    for match in matches:
        if 'USA' in match.team_home:
            match.team_home = match.team_home.replace('USA', 'United States')
        if 'USA' in match.team_away:
            match.team_away = match.team_away.replace('USA', 'United States')
    
    db.session.commit()
    print(f"Updated {len(matches)} matches")
```

### Manual Update for One Match

```python
from backend.app import app
from backend.models import db, Match

with app.app_context():
    # Find match
    match = Match.query.filter_by(team_home='Qatar', team_away='Ecuador').first()
    
    if match:
        match.home_score = 0
        match.away_score = 2
        match.is_finished = True
        
        # Calculate points for predictions
        for prediction in match.predictions:
            prediction.points_earned = prediction.calculate_points()
        
        db.session.commit()
        print("Match updated!")
```

## ✅ Expected Result

After running the fix:
- ✅ ~48 matches marked as finished
- ✅ All finished matches have scores
- ✅ Prediction points calculated
- ✅ Leaderboard updated

## 🔄 On Render

If your app is on Render:

1. **Redeploy** to trigger automatic backfill:
   - Render Dashboard → Your Service → Manual Deploy

2. **Or use Admin Panel**:
   - Login → Admin Panel → Backfill Results

3. **Check Render Logs**:
   - Should see: "✓ Backfilled X historical match result(s)"

## 📝 Quick Commands

```bash
# Local: Run fix script
python3 backend/fix_matches.py

# Render: Trigger via API
curl -X POST https://your-app.onrender.com/api/admin/backfill-results \
  --cookie "session=YOUR_SESSION"

# Check results
curl https://your-app.onrender.com/api/matches | grep is_finished
```

---

**Still having issues?** The team names in your database might not match the API. Check the team names section above.