# Render PostgreSQL Migration Guide

## 🎯 Quick Steps for Render Deployment

### Step 1: Push Your Code
```bash
cd /home/debobrod/Desktop/worldcup-predictor
git add .
git commit -m "Add ESPN API, user predictions view, and live streaming features"
git push origin main
```

Render will automatically detect the changes and start deploying.

---

### Step 2: Run Database Migration

**On Render Dashboard:**

1. Go to https://dashboard.render.com
2. Click on your Web Service
3. Click the **"Shell"** tab (top right corner)
4. In the shell, type:
   ```bash
   python migrate_render_postgres.py
   ```
5. Press Enter and wait for the success message

**Expected Output:**
```
============================================================
  DATABASE MIGRATION FOR RENDER POSTGRESQL
============================================================

🔗 Connecting to database...
✅ Connected to PostgreSQL database successfully!

🔄 Adding new columns to 'match' table...
  ✅ Added column: live_stream_url
  ✅ Added column: espn_match_id

✅ Migration completed successfully!

📊 Database is now ready for new features:
  ✓ Live streaming URLs
  ✓ ESPN API integration
  ✓ User predictions view

🎉 All done! Your database is ready for the new features.
```

---

### Step 3: Verify Deployment

**Check Logs:**
1. Go to "Logs" tab in Render
2. Look for these messages:
   ```
   ✅ ESPN match result auto-updater started (runs every 60 minutes)
   ✅ Database tables checked/created
   ```

**Test Features:**
1. Open your app URL
2. Login as admin
3. Check new "User Predictions" tab
4. Try setting a live stream URL for a match

---

## 🔍 Why This Works

The `migrate_render_postgres.py` script:
- ✅ Automatically reads `DATABASE_URL` from Render environment
- ✅ No need to enter credentials manually
- ✅ Handles Render's postgres:// URL format
- ✅ Safely adds columns with `IF NOT EXISTS`
- ✅ Verifies migration success

---

## 🐛 Troubleshooting

### Issue: "DATABASE_URL not found"
**Solution:** You're not running on Render. Use the Render Shell, not your local terminal.

### Issue: "Columns already exist"
**Solution:** Migration already ran successfully. No action needed!

### Issue: "Permission denied"
**Solution:** Check that your Render database user has ALTER TABLE permissions.

### Issue: Migration script not found
**Solution:** Make sure you pushed all files to Git and Render deployed them.

---

## 📊 What Gets Added to Database

Two new columns in the `match` table:

| Column Name | Type | Purpose |
|------------|------|---------|
| `live_stream_url` | VARCHAR(500) | Stores live streaming URL |
| `espn_match_id` | VARCHAR(100) | Tracks ESPN API match ID |

---

## ✅ Verification Checklist

After migration, verify:

- [ ] Migration script ran without errors
- [ ] Render service restarted successfully
- [ ] ESPN updater shows in logs
- [ ] Admin can access "User Predictions" tab
- [ ] Can set live stream URLs for matches
- [ ] Live stream button appears on started matches

---

## 🎉 Success!

Once you see the success message, your database is ready!

**Next Steps:**
1. Test the new features
2. Read `NEW_FEATURES_GUIDE.md` for usage instructions
3. Announce new features to your users

---

## 💡 Pro Tips

**Automatic Updates:**
- ESPN scores update every 60 minutes automatically
- No manual intervention needed
- Check logs to monitor updates

**Live Streaming:**
- Default URL: `https://cricboost.pages.dev/?id=h`
- Customize per match in admin panel
- URLs auto-generate if not provided

**User Predictions:**
- View by match or view all
- See predictions before matches start
- Track points earned after matches

---

**Made with Bob** 🤖