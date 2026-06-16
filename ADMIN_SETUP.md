# 🔧 Admin Panel Setup Guide

## Overview

The admin panel allows you to:
- View dashboard statistics
- Add, edit, and delete matches
- Update match results and calculate points
- View all users and their statistics

## Step 1: Create an Admin User

After setting up the application, you need to create an admin user. There are two ways to do this:

### Option A: Using Python Shell (Recommended)

1. Make sure your backend server is running
2. Open a new terminal in the `worldcup-predictor` directory
3. Activate your virtual environment:
   ```bash
   source venv/bin/activate  # Linux/Mac
   # OR
   venv\Scripts\activate     # Windows
   ```

4. Run Python and execute these commands:
   ```bash
   cd backend
   python
   ```

5. In the Python shell, type:
   ```python
   from app import app, db
   from models import User
   
   with app.app_context():
       # Create admin user
       admin = User(username='admin', email='debobroto.dutta@gmail.com')
       admin.set_password('admin1@3$5')  # Change this password!
       admin.is_admin = True
       
       db.session.add(admin)
       db.session.commit()
       
       print("Admin user created successfully!")
   ```

6. Press `Ctrl+D` or type `exit()` to exit Python shell

### Option B: Modify an Existing User

If you already have a user account and want to make it admin:

1. Open Python shell as shown above
2. Run:
   ```python
   from app import app, db
   from models import User
   
   with app.app_context():
       # Find user by username
       user = User.query.filter_by(username='your_username').first()
       
       if user:
           user.is_admin = True
           db.session.commit()
           print(f"{user.username} is now an admin!")
       else:
           print("User not found")
   ```

## Step 2: Access the Admin Panel

1. Make sure both backend and frontend servers are running
2. Open your browser and go to:
   ```
   http://localhost:8000/admin.html
   ```

3. You'll be redirected to login if not already logged in
4. Login with your admin credentials
5. You'll be redirected back to the admin panel

## Step 3: Using the Admin Panel

### Dashboard Tab
- View total users, matches, completed matches, and predictions
- Quick overview of your application statistics

### Manage Matches Tab
- **Add New Match**: Click "+ Add New Match" button
  - Enter home team and away team names
  - Select match date and time
  - Choose the tournament stage
  - Click "Save Match"

- **Edit Match**: Click "Edit" button on any match
  - Modify match details
  - Click "Save Match"

- **Delete Match**: Click "Delete" button
  - Confirm deletion
  - Note: This will also delete all predictions for that match

### Update Results Tab
- Shows all matches that have started
- Click "Add Result" or "Update Result" on any match
- Enter the final scores
- Click "Update Result & Calculate Points"
- Points will be automatically calculated for all predictions

### Users Tab
- View all registered users
- See their points, predictions, and admin status
- Monitor user activity

## Important Notes

### Security
- **Change the default admin password immediately!**
- Keep admin credentials secure
- Only trusted users should have admin access

### Best Practices
1. Add all matches before the tournament starts
2. Update results as soon as matches finish
3. Double-check scores before submitting
4. Backup your database regularly

### Troubleshooting

**"Access denied. Admin privileges required"**
- Make sure you set `is_admin = True` for your user
- Logout and login again

**"Please login first"**
- You need to login through the main site first
- Then access admin.html

**Changes not showing**
- Refresh the page
- Check browser console for errors
- Make sure backend server is running

**Can't create matches**
- Verify you're logged in as admin
- Check that all required fields are filled
- Ensure date format is correct

## Database Backup

Before making major changes, backup your database:

```bash
# From the backend directory
cp worldcup.db worldcup.db.backup
```

To restore:
```bash
cp worldcup.db.backup worldcup.db
```

## Adding Multiple Matches Quickly

You can modify `backend/seed_data.py` to add your own matches, then run:

```bash
cd backend
python seed_data.py
```

## Admin API Endpoints

The admin panel uses these protected endpoints:

- `POST /api/matches` - Create match
- `PUT /api/matches/<id>` - Update match
- `DELETE /api/matches/<id>` - Delete match
- `PUT /api/matches/<id>/result` - Update result

All require admin authentication.

## Next Steps

1. ✅ Create admin user
2. ✅ Login to admin panel
3. ✅ Add World Cup 2026 matches
4. ✅ Share main site with friends
5. ✅ Update results as matches finish
6. ✅ Monitor leaderboard

---

**Your admin panel is ready! Start managing your World Cup predictor! ⚽🔧**