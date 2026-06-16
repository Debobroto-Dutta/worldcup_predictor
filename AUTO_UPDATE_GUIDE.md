# Automatic Match Result Updates Guide

## Overview

Your World Cup Predictor now includes **automatic match result updates** from API-Football! The app will automatically fetch and update match results every 15 minutes during the tournament.

## How It Works

1. **Scheduled Updates**: Every 15 minutes, the app checks for finished matches
2. **API Integration**: Fetches results from API-Football (RapidAPI)
3. **Automatic Points**: Calculates and updates user points automatically
4. **Fallback**: Manual updates still work via admin panel

## Setup Instructions

### Step 1: Get Your Free API Key

1. Go to [RapidAPI - API-Football](https://rapidapi.com/api-sports/api/api-football)
2. Sign up for a free account
3. Subscribe to the **FREE plan** (100 requests/day)
4. Copy your API key from the dashboard

### Step 2: Add API Key to Render

1. Go to your Render dashboard
2. Select your web service
3. Click "Environment" tab
4. Add new environment variable:
   - **Key**: `FOOTBALL_API_KEY`
   - **Value**: Your RapidAPI key
5. Click "Save Changes"
6. Service will automatically redeploy

### Step 3: Verify It's Working

Check your Render logs for:
```
✅ Automatic match result updater initialized
✅ Match result auto-updater started (runs every 15 minutes)
```

## Features

### Automatic Updates
- ✅ Checks for finished matches every 15 minutes
- ✅ Updates match scores automatically
- ✅ Calculates user points instantly
- ✅ Works for all match statuses (Full Time, Extra Time, Penalties)

### Manual Fallback
- ✅ Admin panel still works for manual updates
- ✅ API endpoint available: `PUT /api/matches/<id>/result`
- ✅ No API key required for manual updates

### Smart Matching
- ✅ Matches teams by name (fuzzy matching)
- ✅ Only updates unfinished matches
- ✅ Prevents duplicate updates

## API Limits

### Free Tier (100 requests/day)
- **Update frequency**: Every 15 minutes
- **Daily requests**: ~96 requests (well within limit)
- **Cost**: FREE

### If You Need More
- **Pro Plan**: 3,000 requests/day ($9.99/month)
- **Ultra Plan**: 10,000 requests/day ($29.99/month)

## Monitoring

### Check Logs in Render
```
✅ Updated: USA 2-1 Mexico
✅ Successfully updated 3 match(es)
ℹ️  No matches needed updating
⚠️  FOOTBALL_API_KEY not set. Skipping auto-update.
```

### Manual Trigger (if needed)
You can manually trigger an update via Python shell in Render:
```python
from backend.match_updater import MatchUpdater
from backend.app import app

updater = MatchUpdater(app)
updater.update_match_results()
```

## Troubleshooting

### Issue: "FOOTBALL_API_KEY not set"
**Solution**: Add the environment variable in Render dashboard

### Issue: "No matches found from API"
**Solution**: 
- Check if matches are scheduled for today
- Verify API key is correct
- Check RapidAPI dashboard for quota

### Issue: Updates not working
**Solution**:
1. Check Render logs for errors
2. Verify API key is active
3. Check if you've exceeded free tier limit
4. Use manual update as fallback

### Issue: Wrong match updated
**Solution**: 
- Ensure team names in database match API names
- Use manual update for specific matches
- Check logs for matching details

## Manual Update (Fallback)

If automatic updates fail, use the admin panel or API:

```bash
curl -X PUT https://your-app.onrender.com/api/matches/1/result \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your-session-cookie" \
  -d '{"home_score": 2, "away_score": 1}'
```

## Configuration

### Change Update Frequency

Edit `backend/match_updater.py`:
```python
# Change from 15 minutes to 30 minutes
scheduler.add_job(
    func=updater.update_match_results,
    trigger=IntervalTrigger(minutes=30),  # Change this
    ...
)
```

### Disable Auto-Updates

Remove or comment out in `backend/app.py`:
```python
# try:
#     from backend.match_updater import setup_scheduler
#     scheduler = setup_scheduler(app)
# except Exception as e:
#     pass
```

## API Details

### Endpoint Used
```
GET https://api-football-v1.p.rapidapi.com/v3/fixtures
```

### Parameters
- `league`: 1 (FIFA World Cup)
- `season`: 2026
- `date`: YYYY-MM-DD (today's date)

### Response Format
```json
{
  "response": [
    {
      "fixture": {
        "status": {"short": "FT"}
      },
      "teams": {
        "home": {"name": "USA"},
        "away": {"name": "Mexico"}
      },
      "goals": {
        "home": 2,
        "away": 1
      }
    }
  ]
}
```

## Benefits

✅ **No Manual Work**: Results update automatically  
✅ **Real-time Points**: Users see points immediately  
✅ **Reliable**: Falls back to manual if API fails  
✅ **Free**: 100 requests/day is plenty  
✅ **Easy Setup**: Just add API key  

## Support

- **API Documentation**: https://www.api-football.com/documentation-v3
- **RapidAPI Dashboard**: https://rapidapi.com/developer/dashboard
- **Free API Key**: https://rapidapi.com/api-sports/api/api-football

---

**Your World Cup Predictor now updates automatically! 🚀⚽**