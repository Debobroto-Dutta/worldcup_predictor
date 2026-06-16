# Quick Fix for Network Error

The network error when logging in is likely due to one of these issues:

## 1. Database Not Initialized

The database tables might not exist yet. To fix:

### On Render Dashboard:

1. Go to your web service
2. Click on "Shell" tab
3. Run these commands:

```bash
python init_render_db.py
```

This will:
- Create all database tables
- Create a default admin user (username: `admin`, password: `admin123`)

### Alternative - Manual Initialization:

```bash
python -c "from backend.app import app, db; app.app_context().push(); db.create_all(); print('Database created')"
```

Then create a user via the API or register through the website.

## 2. Check Render Logs

1. Go to Render Dashboard → Your Service → Logs
2. Look for any errors when you try to login
3. Common errors:
   - `no such table: user` → Database not initialized
   - `CORS error` → Already fixed in latest code
   - `500 Internal Server Error` → Check database connection

## 3. Test the API Directly

Open your browser console (F12) and run:

```javascript
fetch(window.location.origin + '/api/health')
  .then(r => r.json())
  .then(d => console.log(d))
  .catch(e => console.error(e))
```

If this works, the API is running. If not, check Render logs.

## 4. Register a New User First

Instead of logging in, try registering a new user first:
1. Click "Register" tab
2. Fill in username, email, password
3. Submit
4. Then try logging in with those credentials

## 5. Check Browser Console

Open browser console (F12) and look for:
- Network errors (red text)
- CORS errors
- Failed fetch requests
- Any JavaScript errors

## 6. Verify Environment Variables

In Render Dashboard, check that these are set:
- `SECRET_KEY` - Should be set (auto-generated or custom)
- `DATABASE_URL` - Should be set if using PostgreSQL

## After Fixing

Once the database is initialized:

1. **Test Registration**: Create a new account
2. **Test Login**: Login with the new account
3. **Access Admin**: If you used `init_render_db.py`, login as admin/admin123
4. **Change Admin Password**: Immediately change the default admin password!

## Still Having Issues?

Share the error from:
1. Browser console (F12 → Console tab)
2. Render logs (Dashboard → Logs)

This will help identify the exact problem.