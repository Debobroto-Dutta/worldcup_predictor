# Fix Render PostgreSQL Database - Remove 2022 Data

## The Issue
Your app is deployed on Render with a PostgreSQL database that contains 2022 World Cup data. The local SQLite database fix doesn't affect your production database.

## Solution: Run the Script on Render

You have two options to fix the Render database:

---

## Option 1: Run Script via Render Shell (Recommended)

### Step 1: Access Render Shell
1. Go to your Render dashboard: https://dashboard.render.com
2. Select your web service (worldcup-predictor)
3. Click on the **"Shell"** tab in the left sidebar
4. This opens a terminal connected to your deployed app

### Step 2: Run the Load Script
In the Render shell, run:
```bash
python backend/load_2026_matches.py
```

This will:
- Clear all 2022 matches from your PostgreSQL database
- Load 71 matches for 2026 World Cup
- Update the production database

### Step 3: Restart the Service
After the script completes:
1. Go to the "Settings" tab
2. Click "Manual Deploy" → "Clear build cache & deploy"
3. Or just click "Restart Service"

---

## Option 2: Connect Locally to Render Database

### Step 1: Get Database URL
1. Go to Render dashboard
2. Click on your PostgreSQL database
3. Copy the "External Database URL"

### Step 2: Set Environment Variable
```bash
cd worldcup-predictor
export DATABASE_URL="your-postgres-url-here"
```

### Step 3: Run the Script
```bash
source venv/bin/activate
python backend/load_2026_matches.py
```

This will connect to your Render PostgreSQL database and fix it.

---

## Option 3: Deploy and Auto-Run

### Step 1: Push Changes to GitHub
```bash
cd worldcup-predictor
git push origin main
```

### Step 2: Create a One-Time Job on Render
1. In Render dashboard, go to your service
2. Click "Manual Deploy" → "Deploy latest commit"
3. Once deployed, use the Shell to run the script

---

## Verification

After running the script, verify the fix:

1. **Check via Render Shell:**
```bash
python -c "from backend.app import app; from backend.models import db, Match; 
with app.app_context():
    count = Match.query.count()
    first = Match.query.first()
    print(f'Total: {count}')
    if first:
        print(f'First match: {first.team_home} vs {first.team_away} on {first.match_date}')"
```

2. **Check your live app:**
   - Visit your deployed app URL
   - You should see only 2026 matches
   - No 2022 data should appear

---

## Important Notes

- ✅ The `match_updater.py` has been updated to filter out 2022 matches
- ✅ Even if the API returns 2022 data, it will be ignored
- ✅ Your app will only sync 2026 matches going forward
- ⚠️ You must run the load script on Render to fix the existing data

---

## Quick Command Reference

**Access Render Shell:**
Dashboard → Your Service → Shell tab

**Run the fix:**
```bash
python backend/load_2026_matches.py
```

**Verify:**
```bash
python -c "from backend.app import app; from backend.models import Match; 
with app.app_context(): print(f'Matches: {Match.query.count()}')"
```

**Restart service:**
Dashboard → Settings → Restart Service

---

## Troubleshooting

**If script fails:**
- Check that DATABASE_URL environment variable is set on Render
- Verify PostgreSQL database is running
- Check Render logs for errors

**If still seeing 2022 data:**
- Clear browser cache (Ctrl+Shift+R)
- Verify script ran successfully in Render shell
- Check Render logs to ensure app restarted

---

Created: June 16, 2026
Purpose: Fix production PostgreSQL database on Render