# Remove URLs from Past Matches - API Method (No Shell Access Needed!)

## ✅ New Admin API Endpoints Added

Two new endpoints have been added to your app that you can call directly from your browser or using curl/Postman.

### Endpoint 1: Check Finished Matches with URLs
**GET** `/api/admin/check-past-match-urls`

Shows you all finished matches that have URLs (without removing them).

### Endpoint 2: Remove URLs from Finished Matches
**POST** `/api/admin/remove-past-match-urls`

Removes URLs from all finished matches and returns the list of affected matches.

---

## How to Use (3 Easy Methods)

### Method 1: Using Your Browser (Easiest!)

1. **Login to your admin account** on your Render app
   - Go to: `https://your-app.onrender.com`
   - Login with your admin credentials

2. **Check which matches have URLs** (optional)
   - Open a new tab and go to:
   ```
   https://your-app.onrender.com/api/admin/check-past-match-urls
   ```
   - This shows you all finished matches with URLs

3. **Remove the URLs**
   - You'll need to use the browser console or a tool like Postman for POST requests
   - See Method 2 or 3 below

### Method 2: Using Browser Console

1. **Login to your admin account** first

2. **Open Browser Console** (F12 or Right-click → Inspect → Console)

3. **Run this JavaScript code:**
   ```javascript
   fetch('/api/admin/remove-past-match-urls', {
       method: 'POST',
       credentials: 'include',
       headers: {
           'Content-Type': 'application/json'
       }
   })
   .then(response => response.json())
   .then(data => {
       console.log('Success:', data);
       alert(`Removed URLs from ${data.removed_count} matches!`);
   })
   .catch(error => console.error('Error:', error));
   ```

4. **Check the response** - it will show you how many URLs were removed

### Method 3: Using curl (Command Line)

1. **First, login and get your session cookie:**
   ```bash
   curl -c cookies.txt -X POST https://your-app.onrender.com/api/login \
     -H "Content-Type: application/json" \
     -d '{"username":"your_admin_username","password":"your_admin_password"}'
   ```

2. **Check finished matches with URLs:**
   ```bash
   curl -b cookies.txt https://your-app.onrender.com/api/admin/check-past-match-urls
   ```

3. **Remove URLs from finished matches:**
   ```bash
   curl -b cookies.txt -X POST https://your-app.onrender.com/api/admin/remove-past-match-urls
   ```

### Method 4: Using Postman

1. **Login first:**
   - POST to `https://your-app.onrender.com/api/login`
   - Body (JSON):
     ```json
     {
       "username": "your_admin_username",
       "password": "your_admin_password"
     }
     ```
   - Save the session cookie

2. **Check matches (optional):**
   - GET to `https://your-app.onrender.com/api/admin/check-past-match-urls`
   - Include the session cookie

3. **Remove URLs:**
   - POST to `https://your-app.onrender.com/api/admin/remove-past-match-urls`
   - Include the session cookie

---

## Response Examples

### Check Endpoint Response:
```json
{
  "count": 3,
  "matches": [
    {
      "id": 1,
      "home": "Brazil",
      "away": "Argentina",
      "date": "2026-06-11T12:00:00",
      "score": "2-1",
      "url": "https://cricboost.pages.dev/?id=h"
    },
    ...
  ]
}
```

### Remove Endpoint Response:
```json
{
  "message": "Successfully removed URLs from 3 finished matches",
  "removed_count": 3,
  "matches": [
    {
      "id": 1,
      "home": "Brazil",
      "away": "Argentina",
      "date": "2026-06-11T12:00:00",
      "score": "2-1",
      "url_removed": "https://cricboost.pages.dev/?id=h"
    },
    ...
  ]
}
```

---

## Important Notes

- ✅ **Admin access required** - You must be logged in as an admin
- ✅ **Safe operation** - Only removes URLs from finished matches
- ✅ **Reversible** - URLs can be re-added if needed
- ✅ **No shell access needed** - Works directly through the web API
- ✅ **Already deployed** - The endpoints are now live on your Render app

---

## Troubleshooting

### "Admin access required" error
- Make sure you're logged in as an admin user
- Check that your session cookie is being sent

### "No finished matches with URLs found"
- This is good! It means your database is already clean
- Or no matches have been marked as finished yet

### CORS errors
- Make sure you're calling the API from the same domain
- Or use curl/Postman instead of browser fetch

---

## Quick Start (Recommended)

**Easiest way to remove URLs:**

1. Login to your app as admin
2. Open browser console (F12)
3. Paste this code:
   ```javascript
   fetch('/api/admin/remove-past-match-urls', {
       method: 'POST',
       credentials: 'include'
   }).then(r => r.json()).then(d => alert(d.message));
   ```
4. Done! ✅

---

## Files Modified

- ✅ `backend/app.py` - Added two new admin endpoints:
  - `/api/admin/check-past-match-urls` (GET)
  - `/api/admin/remove-past-match-urls` (POST)

## Next Steps

After removing URLs, consider preventing them from being added to finished matches in the future. See `URL_REMOVAL_REPORT.md` for code modifications.

---
*Last updated: 2026-06-16*