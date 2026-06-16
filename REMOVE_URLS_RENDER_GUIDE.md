# Remove URLs from Past Matches - Render PostgreSQL Guide

## Quick Start

### Option 1: Run on Render Shell (Recommended)

1. **Go to your Render Dashboard**
   - Navigate to your service
   - Click on "Shell" tab

2. **Run the cleanup script**
   ```bash
   python remove_urls_production.py
   ```

3. **Follow the prompts**
   - The script will show you all finished matches with URLs
   - Type `yes` to confirm removal
   - Verification will run automatically

### Option 2: Run Locally with Render Database

1. **Get your DATABASE_URL from Render**
   - Go to Render Dashboard
   - Your Service → Environment tab
   - Copy the `DATABASE_URL` value

2. **Set the environment variable locally**
   ```bash
   export DATABASE_URL='your_postgres_url_here'
   ```

3. **Install PostgreSQL driver (if not installed)**
   ```bash
   pip install psycopg2-binary
   ```

4. **Run the script**
   ```bash
   cd worldcup-predictor
   python remove_urls_production.py
   ```

### Option 3: Direct SQL Query (Advanced)

If you prefer to run SQL directly:

1. **Connect to your Render PostgreSQL database** using any PostgreSQL client

2. **Run this query to see finished matches with URLs:**
   ```sql
   SELECT id, team_home, team_away, match_date, home_score, away_score, live_stream_url
   FROM match
   WHERE is_finished = TRUE AND live_stream_url IS NOT NULL;
   ```

3. **Remove URLs from finished matches:**
   ```sql
   UPDATE match
   SET live_stream_url = NULL
   WHERE is_finished = TRUE AND live_stream_url IS NOT NULL;
   ```

4. **Verify the cleanup:**
   ```sql
   SELECT COUNT(*) as remaining_urls
   FROM match
   WHERE is_finished = TRUE AND live_stream_url IS NOT NULL;
   ```
   Should return 0.

## What the Script Does

1. ✅ Connects to your Render PostgreSQL database
2. ✅ Checks if the `live_stream_url` column exists
3. ✅ Finds all finished matches that have URLs
4. ✅ Shows you the matches before making changes
5. ✅ Asks for confirmation
6. ✅ Removes URLs from finished matches only
7. ✅ Verifies the cleanup was successful

## Safety Features

- **Read-only preview**: Shows matches before making changes
- **Confirmation required**: Won't delete anything without your approval
- **Only finished matches**: Leaves URLs on upcoming/live matches
- **Verification**: Confirms cleanup was successful

## Troubleshooting

### "DATABASE_URL not found"
- **On Render**: DATABASE_URL is set automatically, just run the script
- **Locally**: You need to export the DATABASE_URL first

### "psycopg2 not installed"
```bash
pip install psycopg2-binary
```

### "Connection refused"
- Check if your Render database is running
- Verify DATABASE_URL is correct
- Check firewall/network settings

### "No finished matches found"
- This is good! It means no cleanup is needed
- Or matches haven't been marked as finished yet

## Prevent Future Issues

To prevent URLs from being added to finished matches, modify `backend/app.py`:

**Line 444-445, change from:**
```python
if not match.live_stream_url and match.match_date <= datetime.utcnow():
    match.live_stream_url = f"https://cricboost.pages.dev/?id=h"
```

**To:**
```python
if not match.live_stream_url and match.match_date <= datetime.utcnow() and not match.is_finished:
    match.live_stream_url = f"https://cricboost.pages.dev/?id=h"
```

This ensures URLs are only set for live/upcoming matches, not finished ones.

## Files Created

1. **`remove_urls_production.py`** - Production cleanup script for PostgreSQL
2. **`remove_urls_from_past_matches.py`** - Local cleanup script for SQLite
3. **`REMOVE_URLS_RENDER_GUIDE.md`** - This guide
4. **`URL_REMOVAL_REPORT.md`** - Detailed analysis and findings

## Need Help?

If you encounter issues:
1. Check the Render logs for error messages
2. Verify your DATABASE_URL is correct
3. Ensure the database is accessible
4. Check if the `match` table exists

---
*Last updated: 2026-06-16*