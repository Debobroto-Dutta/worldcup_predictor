# Revert Files to Working State

This guide will help you revert the files back to when the application was working (commit `9f5d085`).

## 🔄 Quick Revert (Recommended)

### Option 1: Revert Specific Files Only

Run these commands to revert only the files that changed:

```bash
cd worldcup-predictor

# Revert backend/app.py to working state
git checkout 9f5d085 -- backend/app.py

# Revert requirements.txt to working state
git checkout 9f5d085 -- requirements.txt

# Revert render.yaml to working state
git checkout 9f5d085 -- render.yaml

# Remove files that were added after working state
rm -f backend/seed_data.py
rm -f init_render_db.py
rm -f frontend/test.html
rm -f ADD_MATCHES_GUIDE.md
rm -f QUICK_FIX.md
rm -f RENDER_DATABASE_FIX.md
rm -f RENDER_FIX.md
```

### Option 2: Full Revert to Working Commit

If you want to completely revert to the working state:

```bash
cd worldcup-predictor

# Create a backup branch first (optional but recommended)
git branch backup-before-revert

# Hard reset to working commit
git reset --hard 9f5d085

# If you've already pushed changes and need to force push
git push origin main --force
```

## 📊 What Changed After Working State

The following files were modified or added after commit `9f5d085`:

**Modified Files:**
- `backend/app.py` - Added automatic match seeding logic
- `requirements.txt` - Added psycopg2-binary
- `render.yaml` - Modified deployment configuration

**Added Files:**
- `backend/seed_data.py` - Match seeding script
- `init_render_db.py` - Database initialization script
- `frontend/test.html` - Test page
- `ADD_MATCHES_GUIDE.md` - Documentation
- `QUICK_FIX.md` - Documentation
- `RENDER_DATABASE_FIX.md` - Documentation
- `RENDER_FIX.md` - Documentation

## ✅ Verify the Revert

After reverting, verify the changes:

```bash
# Check current commit
git log --oneline -1

# Should show: 9f5d085 Configure backend to serve frontend and use relative API URLs

# Check file status
git status

# View differences (if any)
git diff
```

## 🗄️ Add Matches via pgAdmin (After Revert)

Once you've reverted to the working state, use the SQL script to add matches:

1. **Connect to your database via pgAdmin**
   - Open pgAdmin
   - Connect to your PostgreSQL database
   - Navigate to your database

2. **Open Query Tool**
   - Right-click on your database
   - Select "Query Tool"

3. **Run the SQL Script**
   - Open the file: `add_matches_pgadmin.sql`
   - Copy all contents
   - Paste into pgAdmin Query Tool
   - Click "Execute" (F5)

4. **Verify Results**
   - You should see: "Successfully added 119 matches"
   - Check the verification queries at the end of the script

## 🔧 Alternative: Keep Current State but Fix Issues

If you want to keep the current state but just add matches manually:

1. **Don't revert anything**
2. **Use pgAdmin to add matches** (see above)
3. **Or run the Python script:**
   ```bash
   cd worldcup-predictor
   python add_matches_manually.py
   ```

## 📝 Commit History Reference

```
20fcd2a - Add psycopg2-binary and automatic match seeding (CURRENT - BROKEN)
bb34358 - Add automatic match seeding on startup
941c0a7 - database fix
b015c37 - adding database initialization
4190faa - Fix CORS and add database initialization
9f5d085 - Configure backend to serve frontend and use relative API URLs (WORKING ✓)
271de03 - Fix module imports for Render deployment
9f7dc75 - Initial commit
```

## 🚨 Important Notes

1. **Backup First**: Always create a backup branch before reverting
2. **Database**: Reverting code won't affect your database data
3. **Environment Variables**: Make sure your `.env` file is properly configured
4. **Dependencies**: After reverting, run `pip install -r requirements.txt`

## 🆘 If Something Goes Wrong

If the revert causes issues:

```bash
# Go back to the backup branch
git checkout backup-before-revert

# Or go back to the latest commit
git checkout main
git reset --hard origin/main
```

## 📞 Need Help?

If you encounter any issues:
1. Check the git status: `git status`
2. View the current commit: `git log --oneline -1`
3. Check for uncommitted changes: `git diff`

---
Made with Bob