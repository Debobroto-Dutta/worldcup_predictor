# 🔴 Live Match Update Guide

## How to Update Live Matches with Scores and Streaming URLs

This guide shows you how to update matches that are currently LIVE with scores and streaming URLs.

---

## 🎯 Understanding the System

### Live URL Behavior:
- ✅ **Live matches** (started but not finished) → Show live URL
- ❌ **Finished matches** → No live URL (removed automatically)
- ❌ **Future matches** → No live URL yet

### Automatic Updates:
- System checks every 30 minutes
- Adds URLs to live matches
- Removes URLs from finished matches

---

## 📋 Method 1: Using the Update Script (Recommended)

### Step 0: Activate Virtual Environment
```bash
cd /home/debobrod/Desktop/worldcup-predictor

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
pip install -r requirements.txt
```

### Step 1: List All Matches
```bash
python update_live_match.py list
```

**Output:**
```
======================================================================
  ALL MATCHES
======================================================================

ID: 1
   India vs Pakistan
   Date: 2026-06-16 14:30:00
   Score: Not started
   Status: 🔴 Live/Upcoming
   Live URL: No

ID: 2
   Australia vs England
   Date: 2026-06-17 10:00:00
   Score: 250-245
   Status: ✅ Finished
   Live URL: No
```

### Step 2: Update a Live Match
```bash
# Update match with ID 1, scores 150-145
python update_live_match.py 1 150 145

# Or with custom URL
python update_live_match.py 1 150 145 https://cricboost.pages.dev/?id=h
```

**Output:**
```
📊 Updating match: India vs Pakistan
   Match Date: 2026-06-16 14:30:00
   Current Status: Live/Upcoming

✅ Match updated successfully!
   Score: India 150 - 145 Pakistan
   Live URL: https://cricboost.pages.dev/?id=h
   Status: LIVE (not finished)
```

### Step 3: Finish a Match
```bash
# When match is over, mark it as finished
python update_live_match.py finish 1
```

**Output:**
```
📊 Finishing match: India vs Pakistan

✅ Match finished!
   Final Score: India 150 - 145 Pakistan
   Live URL: Removed
   Points calculated for 25 prediction(s)
```

---

## 📋 Method 2: Using Admin Panel

### Via Web Interface:

1. **Go to Admin Panel:**
   ```
   https://your-app-name.onrender.com/admin.html
   ```

2. **Navigate to "Update Results" tab**

3. **Find the live match and click "Update Result"**

4. **Enter scores:**
   - Home Score: 150
   - Away Score: 145

5. **Click "Update Result & Calculate Points"**

**Note:** This marks the match as finished. For live updates, use the script method.

---

## 📋 Method 3: Direct Database Update (Advanced)

### Using Render Shell:

1. Go to Render Dashboard
2. Open your Web Service
3. Click "Shell" tab
4. Run Python:

```python
python
```

Then paste:

```python
from backend.app import app
from backend.models import db, Match

with app.app_context():
    # Update match ID 1
    match = Match.query.get(1)
    
    # Set scores
    match.home_score = 150
    match.away_score = 145
    
    # Mark as live (not finished)
    match.is_finished = False
    
    # Set live URL
    match.live_stream_url = "https://cricboost.pages.dev/?id=h"
    
    db.session.commit()
    print(f"✅ Updated: {match.team_home} {match.home_score}-{match.away_score} {match.team_away}")
```

Press Ctrl+D to exit.

---

## 🔄 Automatic ESPN Updates

The system also fetches scores from ESPN API every 60 minutes:

### Check ESPN Status:
```bash
# Via API
curl https://your-app-name.onrender.com/api/espn-live-status
```

### Manual ESPN Update (Admin):
```bash
# Via API (requires admin login)
curl -X POST https://your-app-name.onrender.com/api/admin/espn-update \
  -H "Cookie: session=YOUR_SESSION"
```

---

## 📊 Complete Workflow Example

### Scenario: India vs Pakistan match is live

**Step 1: Match starts at 2:30 PM**
```bash
# Update with initial scores
python update_live_match.py 1 50 45
```
Result: Live URL appears, users see "🔴 Watch Live Stream" button

**Step 2: Update scores during match**
```bash
# Update at 3:00 PM
python update_live_match.py 1 100 95

# Update at 3:30 PM
python update_live_match.py 1 150 145
```
Result: Scores update, live URL remains

**Step 3: Match finishes**
```bash
# Mark as finished
python update_live_match.py finish 1
```
Result: Live URL removed, points calculated

---

## 🎯 Quick Reference

### List matches:
```bash
python update_live_match.py list
```

### Update live match:
```bash
python update_live_match.py <match_id> <home_score> <away_score>
```

### Finish match:
```bash
python update_live_match.py finish <match_id>
```

### Examples:
```bash
# List all matches
python update_live_match.py list

# Update match 1 with scores 150-145
python update_live_match.py 1 150 145

# Update with custom URL
python update_live_match.py 1 150 145 https://custom-stream.com

# Finish match 1
python update_live_match.py finish 1
```

---

## 🐛 Troubleshooting

### Live URL not showing?
**Check:**
1. Is match marked as NOT finished? (`is_finished = False`)
2. Has match started? (match_date <= now)
3. Is live_stream_url set in database?

**Fix:**
```bash
python update_live_match.py 1 150 145
```

### URL showing on finished match?
**Fix:**
```bash
python update_live_match.py finish 1
```

### Need to check match status?
```bash
python update_live_match.py list
```

---

## 💡 Pro Tips

1. **Update scores regularly** during live matches (every 15-30 minutes)
2. **Always finish matches** when they're over to calculate points
3. **Use the list command** to check current status
4. **Automatic system** handles URLs every 30 minutes, but manual is faster

---

## 🔒 Security Note

The `update_live_match.py` script requires access to your database. Only run it:
- From your local machine with proper credentials
- From Render Shell (has automatic access)
- Never share database credentials publicly

---

**Made with Bob** 🤖