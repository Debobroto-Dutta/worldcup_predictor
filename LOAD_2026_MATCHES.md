# Loading 2026 World Cup Matches

## Overview
This guide explains how to remove 2022 World Cup data and load only 2026 World Cup matches into your database.

## ⚠️ Important: API Returns 2022 Data
The worldcupjson.net API currently returns 2022 World Cup data. To prevent 2022 matches from being synced into your database:

1. **The match_updater.py has been modified** to filter out any matches from 2022
2. **Always use the load_2026_matches.py script** to populate your database with 2026 matches
3. **The automatic sync will skip 2022 matches** thanks to the date filter


## What Was Done

### ✅ Removed All 2022 Data
- Deleted all existing matches from the database
- Deleted all predictions associated with those matches
- Cleared the database completely to start fresh

### ✅ Loaded 2026 World Cup Matches
- Loaded **71 group stage matches** from `schedule.csv`
- All matches are scheduled between June 11-28, 2026
- Includes all participating teams for the 2026 World Cup
- Knockout rounds (Round of 32, Round of 16, etc.) will be added as teams qualify

## How to Run the Script

If you need to reload the 2026 matches or run this on another environment:

```bash
# Navigate to the project directory
cd worldcup-predictor

# Activate virtual environment
source venv/bin/activate

# Run the script
python backend/load_2026_matches.py
```

## What the Script Does

1. **Clears existing data**
   - Removes all predictions (to avoid foreign key conflicts)
   - Removes all matches (including any 2022 data)

2. **Loads 2026 matches from CSV**
   - Reads `schedule.csv` file
   - Parses match information (teams, dates, venues)
   - Creates database entries for each match
   - Skips placeholder matches (knockout rounds TBD)

3. **Summary output**
   - Shows how many matches were loaded
   - Displays breakdown by stage
   - Confirms successful database update

## Match Data Loaded

- **Total Matches**: 71 group stage matches
- **Date Range**: June 11-28, 2026
- **Stage**: Group Stage
- **Status**: All matches marked as not finished (is_finished=False)

## Next Steps

1. **Start your Flask app**:
   ```bash
   python -m backend.app
   ```

2. **Verify the data**:
   - Open your app in a browser
   - You should now see only 2026 World Cup matches
   - No 2022 data should be visible

3. **Users can now**:
   - Make predictions for upcoming 2026 matches
   - View the match schedule
   - Track their points (once matches are played)

4. **Automatic updates**:
   - Match results will auto-update from the API when available
   - The app checks for updates every 15 minutes
   - Manual updates can be done via the admin panel

## Troubleshooting

### If you see 2022 data again:
Run the script again to clear and reload:
```bash
cd worldcup-predictor
source venv/bin/activate
python backend/load_2026_matches.py
```

### If the script fails:
1. Make sure you're in the correct directory
2. Ensure virtual environment is activated
3. Check that `schedule.csv` exists in the project root
4. Verify database connection settings in `.env` file

## File Locations

- **Script**: `backend/load_2026_matches.py`
- **Match Data**: `schedule.csv`
- **Database**: Configured in `.env` file (DATABASE_URL)

## Notes

- The script is safe to run multiple times
- It will always clear existing data before loading new matches
- Knockout round matches will be added automatically as teams qualify
- The API (worldcupjson.net) will provide live updates during the tournament

---

**Created**: June 16, 2026  
**Purpose**: Remove 2022 World Cup data and load 2026 matches only