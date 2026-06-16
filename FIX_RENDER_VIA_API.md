# Fix Render Database via API Endpoint (No Shell Access Needed!)

## Quick Solution - Use the API Endpoint

I've added an admin API endpoint that you can call to fix your Render database without needing shell access!

---

## Step-by-Step Instructions

### Step 1: Push Changes to GitHub
```bash
cd worldcup-predictor
git push origin main
```

### Step 2: Deploy to Render
1. Go to your Render dashboard: https://dashboard.render.com
2. Your service should auto-deploy when you push to GitHub
3. Wait for the deployment to complete (usually 2-3 minutes)
4. Check the deploy logs to ensure it succeeded

### Step 3: Login to Your App as Admin
1. Open your deployed app URL (e.g., https://your-app.onrender.com)
2. Login with your admin account
3. Make sure you're logged in as an admin user

### Step 4: Call the API Endpoint

**Option A: Using Browser Console (Easiest)**

1. While logged into your app, press F12 to open Developer Tools
2. Go to the "Console" tab
3. Paste this code and press Enter:

```javascript
fetch('/api/admin/load-2026-matches', {
    method: 'POST',
    credentials: 'include',
    headers: {
        'Content-Type': 'application/json'
    }
})
.then(response => response.json())
.then(data => {
    console.log('Success:', data);
    alert('Database updated! Refresh the page to see 2026 matches.');
})
.catch(error => {
    console.error('Error:', error);
    alert('Error: ' + error);
});
```

4. You should see a success message
5. Refresh the page - you should now see only 2026 matches!

**Option B: Using curl (From Your Computer)**

First, login and get your session cookie, then:

```bash
curl -X POST https://your-app.onrender.com/api/admin/load-2026-matches \
  -H "Content-Type: application/json" \
  -H "Cookie: session=YOUR_SESSION_COOKIE" \
  --cookie-jar cookies.txt \
  --cookie cookies.txt
```

**Option C: Using Postman or Similar Tool**

1. Open Postman
2. Create a new POST request
3. URL: `https://your-app.onrender.com/api/admin/load-2026-matches`
4. Make sure you're authenticated (login first to get session cookie)
5. Send the request
6. You should get a success response

---

## What This Does

The endpoint will:
1. ✅ Delete all existing matches (including 2022 data)
2. ✅ Delete all predictions (to avoid foreign key issues)
3. ✅ Load 71 group stage matches for 2026 World Cup
4. ✅ Return success message with count of matches added

---

## Verification

After calling the endpoint:

1. **Refresh your app** in the browser
2. You should see only 2026 World Cup matches
3. All matches should be dated June 2026
4. No 2022 matches should appear

---

## Troubleshooting

**"Admin access required" error:**
- Make sure you're logged in as an admin user
- Check that your user account has `is_admin = True` in the database

**"schedule.csv not found" error:**
- Make sure the schedule.csv file is in your repository
- Verify it was deployed to Render (check deploy logs)

**Still seeing 2022 data:**
- Clear your browser cache (Ctrl+Shift+R)
- Make sure the API call succeeded (check response)
- Try calling the endpoint again

**Can't login as admin:**
- You may need to create an admin user first
- Check the SETUP_GUIDE.md for instructions on creating admin users

---

## Alternative: Create Admin User First

If you don't have an admin user yet, you can create one using the Render PostgreSQL console:

1. Go to Render Dashboard → Your PostgreSQL Database
2. Click "Connect" → "External Connection"
3. Use a PostgreSQL client (like pgAdmin or psql) to connect
4. Run this SQL:

```sql
-- Update existing user to admin
UPDATE "user" SET is_admin = true WHERE username = 'your_username';

-- Or create new admin user
INSERT INTO "user" (username, email, password_hash, is_admin, created_at)
VALUES ('admin', 'admin@example.com', 'scrypt:32768:8:1$HASH', true, NOW());
```

Then use that admin account to call the API endpoint.

---

## Summary

✅ **No shell access needed!**
✅ **Just push to GitHub, deploy, and call the API endpoint**
✅ **Works from browser console, curl, or Postman**
✅ **Automatically clears 2022 data and loads 2026 matches**

---

Created: June 16, 2026
Purpose: Fix Render PostgreSQL database without shell access