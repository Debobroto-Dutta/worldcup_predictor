# How to Add Matches to Your Database

## ✨ Automatic Solution (Recommended)

The app now automatically adds matches when it starts up if the database is empty!

### Step 1: Trigger a Redeploy
1. Go to https://dashboard.render.com
2. Click on your `worldcup-predictor` web service
3. Click **"Manual Deploy"** button
4. Select **"Deploy latest commit"**
5. Wait for deployment to complete (2-3 minutes)

### Step 2: Check the Logs
During deployment, you should see in the logs:
```
✓ Database tables initialized
✓ Default admin user created
📅 No matches found. Adding World Cup 2026 schedule...
Successfully added 119 matches to the database!
✓ Matches added successfully!
```

### Step 3: Refresh Your App
1. Go to your app URL
2. Refresh the page
3. You should now see all 119 World Cup 2026 matches!

## Alternative: Manual Method (If Shell Access Available)

If you have shell access and want to run it manually:

### Via Render Shell
1. Go to Render Dashboard → Your web service → **Shell** tab
2. Run: `python backend/seed_data.py`
3. Wait for success message
4. Refresh your app

## What This Does

The seed script adds:
- **72 Group Stage matches** (all teams and groups)
- **16 Round of 32 matches** (TBD teams)
- **8 Round of 16 matches** (TBD teams)
- **4 Quarter Final matches** (TBD teams)
- **2 Semi Final matches** (TBD teams)
- **1 Third Place match** (TBD teams)
- **1 Final match** (TBD teams)

Total: **119 matches** for FIFA World Cup 2026

## Alternative: Use Admin Panel (After Adding Matches)

Once you have matches in the database, you can:
1. Login as admin (username: admin, password: admin123)
2. Go to the admin panel
3. Add, edit, or delete matches manually
4. Update match results when games are played

## Troubleshooting

### If you get "No module named 'backend'"
Try this command instead:
```bash
python -m backend.seed_data
```

### If you get database errors
Make sure the database is properly initialized:
```bash
python init_render_db.py
```
Then run the seed script again.

### If matches still don't show
1. Check the logs for errors
2. Try logging out and logging back in
3. Clear your browser cache
4. Check the API endpoint directly: `https://your-app.onrender.com/api/matches`

## Match Schedule Details

The matches are scheduled from:
- **Start:** June 12, 2026 (Opening match: Mexico vs South Africa)
- **End:** July 20, 2026 (Final)

All times are in UTC. The frontend will display them in the user's local timezone.

## Next Steps After Adding Matches

1. **Change Admin Password:**
   - Login as admin
   - Go to admin panel
   - Change password from default "admin123"

2. **Start Making Predictions:**
   - Users can now see all matches
   - Make predictions before matches start
   - Points are calculated automatically when admins update results

3. **Update Match Results (Admin Only):**
   - As matches are played, login as admin
   - Update the actual scores
   - System automatically calculates points for all predictions

---
Made with Bob