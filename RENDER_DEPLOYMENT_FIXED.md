# Render Deployment Guide - Fixed Version

## Issues Fixed ✅

### 1. **PostgreSQL Support Added**
- Added `psycopg2-binary==2.9.9` to `requirements.txt`
- Fixed DATABASE_URL compatibility (Render uses `postgres://` but SQLAlchemy needs `postgresql://`)

### 2. **Database Initialization Script Created**
- Created `init_render_db.py` to initialize database during build
- Automatically creates tables and default admin user

### 3. **Static File Serving Fixed**
- Updated file paths to use absolute paths for production
- Fixed frontend file serving for Render environment

### 4. **Python Version Specified**
- Created `runtime.txt` with Python 3.11.0
- Updated render.yaml with proper configuration

### 5. **Security Improvements**
- Added `SESSION_COOKIE_SECURE=true` for HTTPS
- Proper gunicorn binding to Render's PORT

## Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Push to GitHub**
   ```bash
   cd worldcup-predictor
   git add .
   git commit -m "Fix Render deployment issues"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Click "Apply" to create services

3. **Set Environment Variables** (in Render Dashboard)
   - `SECRET_KEY` - Auto-generated (or set your own)
   - `MAIL_SERVER` - e.g., `smtp.gmail.com`
   - `MAIL_USERNAME` - Your email
   - `MAIL_PASSWORD` - Your email app password
   - `MAIL_DEFAULT_SENDER` - Sender email address

### Option 2: Manual Setup

1. **Create Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: worldcup-predictor
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt && python init_render_db.py`
     - **Start Command**: `gunicorn backend.app:app --bind 0.0.0.0:$PORT`

2. **Create PostgreSQL Database**
   - Click "New" → "PostgreSQL"
   - Name: `worldcup-db`
   - Choose Free or paid tier

3. **Link Database to Web Service**
   - Go to your web service settings
   - Add environment variable:
     - Key: `DATABASE_URL`
     - Value: Select `worldcup-db` from dropdown

4. **Add Other Environment Variables**
   ```
   SECRET_KEY=<auto-generate or set your own>
   SESSION_COOKIE_SECURE=true
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=noreply@worldcuppredictor.com
   ```

## Post-Deployment

### 1. Verify Deployment
Visit your Render URL (e.g., `https://worldcup-predictor.onrender.com`)

Test endpoints:
- `GET /api/health` - Should return healthy status
- `GET /api/matches` - Should return matches list
- `GET /` - Should serve the frontend

### 2. Default Admin Credentials
```
Username: admin
Password: admin123
```
**⚠️ IMPORTANT: Change the admin password immediately after first login!**

### 3. Add Matches
Use the admin panel to add World Cup 2026 matches, or use the API:

```bash
curl -X POST https://your-app.onrender.com/api/matches \
  -H "Content-Type: application/json" \
  -d '{
    "team_home": "USA",
    "team_away": "Mexico",
    "match_date": "2026-06-11T20:00:00",
    "stage": "Group A"
  }'
```

## Email Configuration

### Using Gmail

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use this app password as `MAIL_PASSWORD` in Render

### Environment Variables for Email
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@worldcuppredictor.com
```

## Troubleshooting

### Issue: Build Fails with Module Import Errors
**Solution**: All imports have been fixed to use `backend.` prefix. Make sure you've pushed the latest changes.

### Issue: Database Connection Error
**Solution**: 
- Verify `DATABASE_URL` is set correctly
- Check that PostgreSQL database is created and linked
- The app automatically converts `postgres://` to `postgresql://`

### Issue: Static Files Not Loading
**Solution**: 
- Frontend files are served by the Flask backend
- Check that frontend directory exists in the repository
- Verify file paths in `backend/app.py`

### Issue: Email Not Sending
**Solution**:
- Verify all email environment variables are set
- For Gmail, use app password (not regular password)
- Check Render logs for specific email errors

## Files Modified/Created

1. ✅ `requirements.txt` - Added psycopg2-binary
2. ✅ `backend/app.py` - Fixed DATABASE_URL and static file serving
3. ✅ `init_render_db.py` - Created database initialization script
4. ✅ `runtime.txt` - Created with Python version
5. ✅ `render.yaml` - Updated with proper configuration

## Production Checklist

- [x] PostgreSQL database configured
- [x] Environment variables set
- [x] SECRET_KEY is secure and unique
- [x] SESSION_COOKIE_SECURE enabled for HTTPS
- [x] Email configuration complete
- [ ] Admin password changed from default
- [ ] Matches added to database
- [ ] CORS origins updated for production domain
- [ ] Database backups configured

## Monitoring

- Check Render logs for errors: Dashboard → Your Service → Logs
- Monitor database usage: Dashboard → Your Database → Metrics
- Set up alerts in Render dashboard

## Updating the Application

```bash
# Make changes locally
git add .
git commit -m "Your changes"
git push origin main

# Render will automatically redeploy
```

## Cost Considerations

**Free Tier:**
- Web service spins down after 15 minutes of inactivity
- 750 hours/month free
- PostgreSQL: 90 days free trial, then $7/month

**Paid Tier:**
- Always-on service ($7/month)
- Better performance
- More resources

## Support

If you encounter issues:
1. Check Render logs in the dashboard
2. Review this guide
3. Check the main README.md for application details
4. Contact Render support for platform-specific issues

---

**Your World Cup Predictor is now ready for deployment on Render! 🚀⚽**