# Render Database Connection Fix

## Root Cause
The error `sqlite3.OperationalError: no such table: user` indicates the app is using SQLite instead of PostgreSQL. This happens when the `DATABASE_URL` environment variable is not properly set.

## Critical Steps to Fix

### Step 1: Verify Database Service Exists
1. Go to https://dashboard.render.com
2. Check if you have a **PostgreSQL database** service named `worldcup-db`
3. If NOT, you need to create one:
   - Click "New +" → "PostgreSQL"
   - Name: `worldcup-db`
   - Database: `worldcup`
   - User: `worldcup`
   - Region: Same as your web service
   - Plan: Free
   - Click "Create Database"

### Step 2: Link Database to Web Service
1. Go to your web service (`worldcup-predictor`)
2. Click "Environment" tab
3. Look for `DATABASE_URL` variable
4. **If it doesn't exist or shows a local path:**
   - Click "Add Environment Variable"
   - Key: `DATABASE_URL`
   - Value: Click "Generate Value" → Select your `worldcup-db` database
   - This will auto-populate with the PostgreSQL connection string
5. Click "Save Changes"

### Step 3: Verify DATABASE_URL Format
The `DATABASE_URL` should look like:
```
postgresql://user:password@host:5432/database
```

NOT like:
```
sqlite:///worldcup.db
```

If it shows SQLite, the database isn't linked properly.

### Step 4: Redeploy with Database Linked
1. After ensuring DATABASE_URL is correct
2. Click "Manual Deploy" → "Clear build cache & deploy"
3. Wait for deployment to complete
4. Check logs for: `✓ Database tables initialized`

## Verification Checklist

Run through this checklist in Render dashboard:

- [ ] PostgreSQL database service `worldcup-db` exists and is running
- [ ] Web service `worldcup-predictor` exists
- [ ] In web service Environment tab, `DATABASE_URL` variable exists
- [ ] `DATABASE_URL` value starts with `postgresql://` (not `sqlite://`)
- [ ] Both services are in the same region
- [ ] Web service has been redeployed after setting DATABASE_URL

## Check Build Logs

After redeploying, check the build logs for:

**Success indicators:**
```
✓ Database tables initialized
✓ Default admin user created
```

**Failure indicators:**
```
sqlite3.OperationalError
No such table: user
```

If you see failure indicators, DATABASE_URL is still not set correctly.

## Alternative: Manual Database URL Setup

If auto-linking doesn't work:

1. Go to your PostgreSQL database service
2. Click "Info" tab
3. Copy the "External Database URL" or "Internal Database URL"
4. Go to web service → Environment
5. Set `DATABASE_URL` to the copied URL
6. Save and redeploy

## Testing After Fix

Once deployed successfully:

1. Visit your app URL
2. Try to register a new user
3. Should work without errors
4. Check logs - should NOT see `sqlite3.OperationalError`

## Common Issues

### Issue: DATABASE_URL keeps reverting to SQLite
**Solution:** The database isn't properly linked in render.yaml. Manually set it in the dashboard.

### Issue: "Connection refused" error
**Solution:** Database service might be in a different region. Both services must be in the same region.

### Issue: Build succeeds but runtime fails
**Solution:** The init script ran during build, but runtime is using a different DATABASE_URL. Check environment variables.

## Current App.py Fix

The app now automatically initializes the database on startup, so you don't need to run `init_render_db.py` separately. Just ensure DATABASE_URL is correct and redeploy.

## Need Help?

If still not working after following all steps:
1. Take a screenshot of your Render Environment variables
2. Take a screenshot of your database service info
3. Share the deployment logs (last 50 lines)

---
Made with Bob