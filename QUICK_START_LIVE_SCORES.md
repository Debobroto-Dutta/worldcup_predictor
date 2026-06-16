# Quick Start: Live Football Scores

## 🚀 Get Started in 5 Minutes

### Step 1: Test API Connection

First, verify the API is working:

```bash
curl https://worldcupjson.net/matches | python3 -m json.tool | head -50
```

You should see match data in JSON format.

### Step 2: Run the Sync Script

Sync all matches from the API to your database:

```bash
cd worldcup-predictor
python3 backend/sync_matches.py
```

This will:
- Test API connection
- Fetch all teams
- Sync all matches to your database
- Show a summary

### Step 3: Start Your App

```bash
python3 -m backend.app
```

The app will:
- Start on http://localhost:5000
- Automatically backfill historical results
- Start the scheduler (updates every 15 minutes)

### Step 4: Test the Endpoints

#### Get Live Scores (Public)
```bash
curl http://localhost:5000/api/live-scores
```

#### Get All Teams (Public)
```bash
curl http://localhost:5000/api/teams
```

#### Get All Matches (Public)
```bash
curl http://localhost:5000/api/matches
```

## 🔧 Admin Functions

### Login as Admin

1. Create an admin user or update existing user in database
2. Login via the web interface
3. Access admin panel

### Sync Matches (Admin Only)

```bash
curl -X POST http://localhost:5000/api/admin/sync-matches \
  -H "Content-Type: application/json" \
  --cookie "session=YOUR_SESSION_COOKIE"
```

Or use the admin panel in your browser.

### Backfill Results (Admin Only)

```bash
curl -X POST http://localhost:5000/api/admin/backfill-results \
  -H "Content-Type: application/json" \
  --cookie "session=YOUR_SESSION_COOKIE"
```

### Test API Connection (Admin Only)

```bash
curl http://localhost:5000/api/admin/test-api \
  --cookie "session=YOUR_SESSION_COOKIE"
```

## 📊 What Happens Automatically

Once your app is running:

1. **Every 15 minutes**: The scheduler checks for finished matches
2. **When a match finishes**: 
   - Scores are updated from API
   - Match is marked as finished
   - All predictions are evaluated
   - Points are calculated automatically

## 🎯 Example: Complete Workflow

### 1. Initial Setup

```bash
# Navigate to project
cd worldcup-predictor

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Sync matches
python3 backend/sync_matches.py
```

### 2. Start App

```bash
python3 -m backend.app
```

You should see:
```
✓ Database tables checked/created
✓ Backfilled X historical match result(s)
✓ Automatic match result updater initialized
✓ Match result auto-updater started (runs every 15 minutes)
```

### 3. Use the App

1. Open browser: http://localhost:5000
2. Register/Login
3. Make predictions
4. Check leaderboard
5. Scores update automatically!

## 🔍 Verify It's Working

### Check Console Logs

You should see periodic updates:
```
✅ Updated: England 2-1 France
✅ Successfully updated 3 match(es)
```

### Check Database

```bash
# If using SQLite
sqlite3 worldcup.db "SELECT team_home, team_away, home_score, away_score, is_finished FROM match LIMIT 5;"
```

### Check API Endpoint

```bash
curl http://localhost:5000/api/matches | python3 -m json.tool
```

Look for matches with `is_finished: true` and scores.

## 🐛 Troubleshooting

### No Matches in Database?

Run the sync script:
```bash
python3 backend/sync_matches.py
```

### Scores Not Updating?

1. Check if scheduler is running (look for startup message)
2. Check API connection:
   ```bash
   curl https://worldcupjson.net/matches
   ```
3. Manually trigger update via admin panel

### Team Names Don't Match?

The API uses these team names:
- England, France, Brazil, Argentina, etc.

Make sure your database matches these names exactly, or update the team_mapping in `match_updater.py`.

## 📱 Frontend Integration

Add this to your frontend JavaScript to show live scores:

```javascript
// Fetch and display live scores
async function updateLiveScores() {
  try {
    const response = await fetch('/api/live-scores');
    const data = await response.json();
    
    const liveScoresDiv = document.getElementById('live-scores');
    
    if (data.live_matches.length > 0) {
      liveScoresDiv.innerHTML = '<h3>🔴 LIVE</h3>';
      data.live_matches.forEach(match => {
        liveScoresDiv.innerHTML += `
          <div class="live-match">
            <span>${match.home_team}</span>
            <span class="score">${match.home_score} - ${match.away_score}</span>
            <span>${match.away_team}</span>
          </div>
        `;
      });
    } else {
      liveScoresDiv.innerHTML = '<p>No live matches</p>';
    }
  } catch (error) {
    console.error('Error fetching live scores:', error);
  }
}

// Update every 30 seconds
setInterval(updateLiveScores, 30000);
updateLiveScores(); // Initial call
```

## 📚 More Information

- Full documentation: [LIVE_SCORES_GUIDE.md](LIVE_SCORES_GUIDE.md)
- API source: https://github.com/rezarahiminia/worldcup2026
- API endpoint: https://worldcupjson.net

## ✅ Success Checklist

- [ ] API connection tested
- [ ] Matches synced to database
- [ ] App running with scheduler
- [ ] Live scores endpoint working
- [ ] Admin panel accessible
- [ ] Automatic updates confirmed

---

**Need help?** Check the full guide in `LIVE_SCORES_GUIDE.md`