# Render Deployment Guide

## Fixed Issues

The main issue was with Python module imports. The error `ModuleNotFoundError: No module named 'models'` occurred because:

1. **Import statements were relative** - Changed from `from models import ...` to `from backend.models import ...`
2. **Gunicorn command in Procfile** - Uses `backend.app:app` which requires proper module structure

## Files Modified

1. **backend/app.py** - Fixed import: `from backend.models import db, User, Match, Prediction`
2. **backend/init_db.py** - Fixed imports to use `backend.` prefix
3. **backend/seed_data.py** - Fixed imports to use `backend.` prefix
4. **backend/migrate_db.py** - Fixed imports to use `backend.` prefix
5. **render.yaml** - Created configuration file for Render
6. **.gitignore** - Updated to exclude database files and virtual environments

## Deployment Steps

### 1. Push Changes to Git

```bash
cd worldcup-predictor
git add .
git commit -m "Fix module imports for Render deployment"
git push origin main
```

### 2. Deploy on Render

#### Option A: Using render.yaml (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml` and configure services
5. Set environment variables in Render dashboard:
   - `SECRET_KEY` (auto-generated or set your own)
   - `MAIL_SERVER` (e.g., smtp.gmail.com)
   - `MAIL_USERNAME` (your email)
   - `MAIL_PASSWORD` (your email app password)
   - `MAIL_DEFAULT_SENDER` (sender email address)

#### Option B: Manual Setup

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: worldcup-predictor
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend.app:app`
   - **Instance Type**: Free (or paid for better performance)

5. Add Environment Variables:
   - `SECRET_KEY`: Generate a secure random string
   - `DATABASE_URL`: Will be auto-set if you add a database
   - `MAIL_SERVER`: smtp.gmail.com (or your mail server)
   - `MAIL_PORT`: 587
   - `MAIL_USE_TLS`: true
   - `MAIL_USERNAME`: Your email address
   - `MAIL_PASSWORD`: Your email app password
   - `MAIL_DEFAULT_SENDER`: noreply@yourdomain.com

### 3. Add PostgreSQL Database (Optional but Recommended)

1. In Render dashboard, click "New" → "PostgreSQL"
2. Name it `worldcup-db`
3. Choose Free tier or paid
4. Once created, go to your web service
5. Add environment variable:
   - Key: `DATABASE_URL`
   - Value: Select "worldcup-db" from dropdown

### 4. Initialize Database

After deployment, you need to initialize the database:

1. Go to your Render service dashboard
2. Click "Shell" tab
3. Run:
```bash
python -m backend.init_db
python -m backend.seed_data
```

Or create an admin user manually through the API.

### 5. Verify Deployment

1. Visit your Render URL (e.g., `https://worldcup-predictor.onrender.com`)
2. You should see the API information page
3. Test endpoints:
   - `GET /api/health` - Should return healthy status
   - `GET /api/matches` - Should return matches list

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

### Issue: Module Import Errors

**Solution**: All imports have been fixed to use `backend.` prefix. Make sure you've pushed the latest changes.

### Issue: Database Not Found

**Solution**: 
1. Check if `DATABASE_URL` environment variable is set
2. Run initialization commands in Render shell
3. For SQLite (not recommended for production), the app will create it automatically

### Issue: Email Not Sending

**Solution**:
1. Verify all email environment variables are set
2. Check if using Gmail app password (not regular password)
3. Check Render logs for specific email errors

### Issue: Static Files Not Loading

**Solution**: 
- Frontend files are static HTML/JS/CSS
- Host them separately on Render Static Site or use the backend to serve them
- Update API URLs in frontend files to point to your Render backend URL

## Production Recommendations

1. **Use PostgreSQL** instead of SQLite for production
2. **Set strong SECRET_KEY** - Use a cryptographically secure random string
3. **Enable HTTPS** - Render provides this automatically
4. **Set up monitoring** - Use Render's built-in monitoring
5. **Configure CORS** - Update CORS settings in `backend/app.py` if needed
6. **Regular backups** - Set up database backups in Render
7. **Environment variables** - Never commit sensitive data to Git

## Updating the Application

```bash
# Make changes locally
git add .
git commit -m "Your changes"
git push origin main

# Render will automatically redeploy
```

## Support

If you encounter issues:
1. Check Render logs in the dashboard
2. Review this guide
3. Check the main README.md for application details
4. Contact Render support for platform-specific issues

## Cost Considerations

- **Free Tier**: 
  - Web service spins down after inactivity
  - 750 hours/month free
  - PostgreSQL: 90 days free, then $7/month

- **Paid Tier**:
  - Always-on service
  - Better performance
  - More resources

Choose based on your needs and budget.