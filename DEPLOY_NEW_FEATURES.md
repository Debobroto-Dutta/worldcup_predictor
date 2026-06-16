# Deploy New Features - Quick Guide

## 🚀 Quick Deployment Steps

### Step 1: Run Database Migration
```bash
cd /home/debobrod/Desktop/worldcup-predictor
python backend/add_live_fields.py
```

This adds the new database columns for live streaming URLs and ESPN match IDs.

### Step 2: Test Locally (Optional)
```bash
# Start the Flask app
python backend/app.py

# Open browser to http://localhost:5000
# Login as admin and test new features
```

### Step 3: Deploy to Production

#### If using Render.com:
1. **Push to Git:**
   ```bash
   git add .
   git commit -m "Add ESPN API, user predictions view, and live streaming features"
   git push origin main
   ```

2. **Run Migration on Render:**
   - Go to Render Dashboard
   - Open your web service
   - Click "Shell" tab
   - Run: `python backend/add_live_fields.py`

3. **Restart Service:**
   - Render will auto-restart after git push
   - Or manually restart from dashboard

#### If using other hosting:
1. Upload all changed files
2. Run the migration script
3. Restart your web server

---

## 📝 Files Changed/Added

### Backend Files:
- ✅ `backend/models.py` - Added live_stream_url and espn_match_id fields
- ✅ `backend/app.py` - Added new API endpoints
- ✅ `backend/espn_updater.py` - NEW: ESPN API integration
- ✅ `backend/add_live_fields.py` - NEW: Database migration script

### Frontend Files:
- ✅ `frontend/app.js` - Added live stream button display
- ✅ `frontend/admin.html` - Added predictions tab and live URL field
- ✅ `frontend/admin.js` - Added prediction viewing functions

### Documentation:
- ✅ `NEW_FEATURES_GUIDE.md` - Complete feature documentation
- ✅ `DEPLOY_NEW_FEATURES.md` - This deployment guide

---

## ✅ Verification Checklist

After deployment, verify:

### 1. Database Migration
- [ ] Run migration script successfully
- [ ] No errors in logs
- [ ] Existing data intact

### 2. ESPN Integration
- [ ] Check logs for "ESPN match result auto-updater started"
- [ ] Manually trigger update from admin panel
- [ ] Verify scores update correctly

### 3. User Predictions View
- [ ] Login as admin
- [ ] Navigate to "User Predictions" tab
- [ ] Verify predictions are visible
- [ ] Test both view modes (by match / all)

### 4. Live Streaming URLs
- [ ] Create/edit a match
- [ ] Set live stream URL
- [ ] Verify URL saves correctly
- [ ] Check button appears when match starts
- [ ] Click button to test URL

---

## 🔍 Testing Commands

### Test ESPN API:
```bash
curl http://localhost:5000/api/espn-live-status
```

### Test Predictions Endpoint (as admin):
```bash
curl -X GET http://localhost:5000/api/admin/predictions \
  -H "Cookie: session=YOUR_SESSION_COOKIE"
```

### Test Live URL Setting (as admin):
```bash
curl -X POST http://localhost:5000/api/matches/1/set-live-url \
  -H "Content-Type: application/json" \
  -H "Cookie: session=YOUR_SESSION_COOKIE" \
  -d '{"live_stream_url": "https://cricboost.pages.dev/?id=h"}'
```

---

## 🐛 Common Issues & Solutions

### Issue: Migration fails with "column already exists"
**Solution:** This is normal if you run migration twice. The columns are already added.

### Issue: ESPN updates not working
**Solution:** 
1. Check internet connectivity
2. Verify ESPN API is accessible
3. Check logs for specific errors
4. Try manual update from admin panel

### Issue: Live stream button not showing
**Solution:**
1. Verify match start time has passed
2. Check if live_stream_url is set in database
3. Clear browser cache
4. Check browser console for errors

### Issue: Predictions not visible in admin panel
**Solution:**
1. Verify you're logged in as admin
2. Check if any predictions exist
3. Refresh the page
4. Check API response in browser network tab

---

## 📊 Monitoring

### Check Application Logs:
```bash
# Look for these messages:
✅ ESPN match result auto-updater started (runs every 60 minutes)
✅ Successfully updated X match(es) from ESPN
✅ Database tables checked/created
```

### Monitor ESPN Updates:
- Updates run automatically every 60 minutes
- Check admin dashboard for last update time
- Manually trigger if needed

### Monitor User Activity:
- Check "User Predictions" tab regularly
- Review prediction patterns
- Verify points calculation

---

## 🎯 Next Steps

After successful deployment:

1. **Announce New Features:**
   - Email users about live streaming
   - Highlight ESPN auto-updates
   - Explain prediction visibility

2. **Monitor Performance:**
   - Watch for any errors
   - Check ESPN API response times
   - Monitor database performance

3. **Gather Feedback:**
   - Ask users about live streaming experience
   - Check if URLs work correctly
   - Adjust based on feedback

---

## 📞 Support

If you encounter issues:

1. Check `NEW_FEATURES_GUIDE.md` for detailed documentation
2. Review application logs for errors
3. Test API endpoints directly
4. Verify database migration completed

---

## 🎉 Success Indicators

You'll know deployment is successful when:

✅ No errors in application logs
✅ ESPN updater shows in startup logs
✅ Admin can view user predictions
✅ Live stream buttons appear on started matches
✅ Scores update automatically every 60 minutes

---

**Ready to deploy? Follow the steps above!** 🚀

**Made with Bob** 🤖