# Live Football Scores Integration Guide

## Overview

Your World Cup Predictor app now has full integration with live football scores from the **worldcupjson.net** API. This free API provides real-time match data, scores, and team information.

## Features

### 1. **Automatic Score Updates**
- Runs every 15 minutes automatically
- Updates finished matches with final scores
- Calculates prediction points automatically
- No manual intervention needed

### 2. **Manual Sync Options**
- Backfill historical results
- Sync all matches from API
- Test API connection
- Manual match updates

### 3. **Live Score Endpoints**
- Get current live matches
- Fetch all teams
- View match details

## API Endpoints

### Public Endpoints

#### Get Live Scores
```http
GET /api/live-scores
```

Returns currently ongoing matches with live scores.

**Response:**
```json
{
  "live_matches": [
    {
      "home_team": "England",
      "away_team": "France",
      "home_score": 1,
      "away_score": 2,
      "status": "second_half",
      "venue": "Al Bayt Stadium",
      "datetime": "2026-06-20T19:00:00Z"
    }
  ],
  "count": 1
}
```

#### Get All Teams
```http
GET /api/teams
```

Returns all World Cup teams organized by group.

**Response:**
```json
{
  "groups": [
    {
      "letter": "A",
      "teams": [
        {
          "country": "QAT",
          "name": "Qatar",
          "group_letter": "A",
          "group_points": 0,
          "wins": 0,
          "draws": 0,
          "losses": 3
        }
      ]
    }
  ]
}
```

### Admin Endpoints (Require Authentication)

#### Sync All Matches
```http
POST /api/admin/sync-matches
```

Syncs all matches from the API to your database. Creates new matches and updates existing ones.

**Response:**
```json
{
  "message": "Sync complete: 5 created, 3 updated",
  "created_count": 5,
  "updated_count": 3
}
```

#### Backfill Results
```http
POST /api/admin/backfill-results
```

Updates all historical match results (even already finished matches).

**Response:**
```json
{
  "message": "Successfully backfilled 48 match(es)",
  "updated_count": 48
}
```

#### Test API Connection
```http
GET /api/admin/test-api
```

Tests the connection to worldcupjson.net API.

**Response:**
```json
{
  "message": "Found 64 matches from API",
  "matches_count": 64,
  "sample_matches": [...]
}
```

## Team Name Mapping

The system includes automatic team name mapping from country codes to full names:

| Code | Team Name |
|------|-----------|
| ENG | England |
| BRA | Brazil |
| ARG | Argentina |
| FRA | France |
| GER | Germany |
| ESP | Spain |
| POR | Portugal |
| NED | Netherlands |
| ... | ... |

## Usage Examples

### Frontend JavaScript

#### Fetch Live Scores
```javascript
async function getLiveScores() {
  try {
    const response = await fetch('/api/live-scores');
    const data = await response.json();
    
    if (data.live_matches.length > 0) {
      console.log('Live matches:', data.live_matches);
      // Update UI with live scores
      displayLiveScores(data.live_matches);
    } else {
      console.log('No live matches currently');
    }
  } catch (error) {
    console.error('Error fetching live scores:', error);
  }
}

// Call every 30 seconds for real-time updates
setInterval(getLiveScores, 30000);
```

#### Sync Matches (Admin)
```javascript
async function syncMatches() {
  try {
    const response = await fetch('/api/admin/sync-matches', {
      method: 'POST',
      credentials: 'include'
    });
    const data = await response.json();
    
    alert(`Sync complete: ${data.created_count} created, ${data.updated_count} updated`);
  } catch (error) {
    console.error('Error syncing matches:', error);
  }
}
```

### Python Script

#### Manual Sync Script
```python
from backend.match_updater import MatchUpdater
from backend.app import app

# Create updater instance
updater = MatchUpdater(app)

# Sync all matches
created, updated = updater.sync_matches_from_api()
print(f"Sync complete: {created} created, {updated} updated")

# Get live scores
live_matches = updater.get_live_scores()
for match in live_matches:
    print(f"{match['home_team']} {match['home_score']}-{match['away_score']} {match['away_team']}")
```

## How It Works

### 1. Automatic Updates (Background Scheduler)

The app automatically runs a background job every 15 minutes:

```python
# In app.py (runs on startup)
from backend.match_updater import setup_scheduler, MatchUpdater

# Backfill historical results first
updater = MatchUpdater(app)
backfilled = updater.backfill_all_results()

# Start scheduler for ongoing updates
scheduler = setup_scheduler(app)
```

### 2. Match Matching Logic

The system uses smart matching to find matches in your database:

1. **Exact Match**: Tries exact team name match first
2. **Fuzzy Match**: Falls back to partial name matching (case-insensitive)
3. **Status Check**: Only updates unfinished matches (unless backfilling)

### 3. Points Calculation

When a match result is updated:

1. Match scores are updated from API
2. Match is marked as finished
3. All user predictions are evaluated
4. Points are calculated automatically:
   - **3 points**: Exact score prediction
   - **1 point**: Correct winner prediction
   - **0 points**: Wrong prediction

## Initial Setup

### Step 1: Sync All Matches

First time setup - sync all matches from the API:

```bash
# Using curl
curl -X POST http://localhost:5000/api/admin/sync-matches \
  -H "Content-Type: application/json" \
  --cookie "session=YOUR_SESSION_COOKIE"

# Or use the admin panel in your frontend
```

### Step 2: Verify Matches

Check that matches were created:

```bash
curl http://localhost:5000/api/matches
```

### Step 3: Test Live Scores

```bash
curl http://localhost:5000/api/live-scores
```

## Troubleshooting

### No Matches Updating?

1. **Check API Connection**:
   ```bash
   curl https://worldcupjson.net/matches
   ```

2. **Test API Endpoint**:
   ```bash
   curl http://localhost:5000/api/admin/test-api
   ```

3. **Check Logs**: Look for error messages in console

### Team Names Don't Match?

If team names in your database don't match the API:

1. Update team names in database to match API exactly
2. Or add mapping in `match_updater.py`:
   ```python
   self.team_mapping = {
       'ENG': 'England',
       'YOUR_CODE': 'Your Team Name',
       # ...
   }
   ```

### Scheduler Not Running?

Check if APScheduler is installed:
```bash
pip install APScheduler==3.10.4
```

## Advanced Configuration

### Change Update Frequency

Edit `match_updater.py`:

```python
# Change from 15 minutes to 5 minutes
scheduler.add_job(
    func=updater.update_match_results,
    trigger=IntervalTrigger(minutes=5),  # Changed from 15
    id='match_updater',
    name='Update match results from API',
    replace_existing=True
)
```

### Add Custom Team Mappings

Edit `match_updater.py`:

```python
self.team_mapping = {
    # Add your custom mappings
    'USA': 'United States',
    'KOR': 'South Korea',
    # ...
}
```

## API Source

- **API**: https://worldcupjson.net
- **GitHub**: https://github.com/rezarahiminia/worldcup2026
- **Free**: No API key required
- **Rate Limits**: Reasonable for free tier

## Best Practices

1. **Don't Poll Too Frequently**: The API updates every few minutes, polling every 30-60 seconds is sufficient
2. **Use Caching**: Cache API responses for 30-60 seconds to reduce load
3. **Handle Errors**: Always handle API errors gracefully
4. **Monitor Usage**: Keep track of API calls to avoid rate limits
5. **Backup Data**: Keep your own database as the source of truth

## Support

For issues or questions:
1. Check the API documentation: https://github.com/rezarahiminia/worldcup2026
2. Review error logs in your console
3. Test API connection with `/api/admin/test-api`

---

**Made with Bob** 🤖