# 🔐 Admin Panel Access Guide

## How to Access the Admin Panel

### Step 1: Go to Admin URL
Open your browser and navigate to:
```
https://your-app-name.onrender.com/admin.html
```

Replace `your-app-name` with your actual Render app name.

**Or locally:**
```
http://localhost:5000/admin.html
```

---

## Step 2: Login with Admin Account

You need an admin user account. Here's how to create one:

### Option A: Create Admin User via Database

**Using Render Shell:**
1. Go to Render Dashboard
2. Open your Web Service
3. Click "Shell" tab
4. Run this Python script:

```python
python
```

Then paste this code:
```python
from backend.app import app, db
from backend.models import User

with app.app_context():
    # Create admin user
    admin = User(
        username='admin',
        email='admin@example.com'
    )
    admin.set_password('your_secure_password')  # Change this!
    admin.is_admin = True
    
    db.session.add(admin)
    db.session.commit()
    
    print("✅ Admin user created!")
    print(f"Username: {admin.username}")
    print(f"Email: {admin.email}")
    print("Password: [the one you set]")
```

Press Ctrl+D to exit Python.

### Option B: Make Existing User Admin

If you already have a user account, make it admin:

**Using Render Shell:**
```python
python
```

Then:
```python
from backend.app import app, db
from backend.models import User

with app.app_context():
    # Find your user (replace 'your_username' with your actual username)
    user = User.query.filter_by(username='your_username').first()
    
    if user:
        user.is_admin = True
        db.session.commit()
        print(f"✅ {user.username} is now an admin!")
    else:
        print("❌ User not found")
```

### Option C: Create Admin Script

Create a file `create_admin.py` in your project:

```python
from backend.app import app, db
from backend.models import User
import sys

def create_admin(username, email, password):
    with app.app_context():
        # Check if user exists
        existing = User.query.filter_by(username=username).first()
        if existing:
            print(f"❌ User '{username}' already exists")
            return False
        
        # Create admin user
        admin = User(username=username, email=email)
        admin.set_password(password)
        admin.is_admin = True
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Admin user created successfully!")
        print(f"Username: {username}")
        print(f"Email: {email}")
        return True

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python create_admin.py <username> <email> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    
    create_admin(username, email, password)
```

Then run:
```bash
python create_admin.py admin admin@example.com YourSecurePassword123
```

---

## Step 3: Login to Admin Panel

1. Go to `https://your-app-name.onrender.com/admin.html`
2. You'll be redirected to login page if not logged in
3. Enter your admin username and password
4. Click "Login"
5. You'll be redirected to the admin panel

---

## Admin Panel Features

Once logged in, you'll see these tabs:

### 📊 Dashboard
- Total users
- Total matches
- Completed matches
- Total predictions

### ⚽ Manage Matches
- Add new matches
- Edit existing matches
- Delete matches
- Set live stream URLs

### 🎯 Update Results
- Update match scores
- Mark matches as finished
- Calculate points automatically

### 👥 User Predictions (NEW!)
- View all predictions by match
- View all predictions by user
- See who predicted what
- Track points earned

### 👤 Users
- View all users
- Edit user details
- Make users admin
- Delete users
- Send password reset emails

---

## Security Tips

1. **Use Strong Password:**
   - At least 12 characters
   - Mix of letters, numbers, symbols
   - Don't use common words

2. **Keep Credentials Safe:**
   - Don't share admin password
   - Change password regularly
   - Use password manager

3. **Admin Access:**
   - Only give admin access to trusted users
   - Review admin users regularly

---

## Troubleshooting

### "Access denied. Admin privileges required."
**Solution:** Your user account is not an admin. Follow Option B above to make your account admin.

### "Please login first"
**Solution:** You're not logged in. Go to the main page and login first, then access `/admin.html`.

### Can't find admin.html
**Solution:** Make sure you pushed all files to Git and Render deployed them. Check that `frontend/admin.html` exists.

### Forgot admin password
**Solution:** Use the password reset feature or create a new admin user using the database method above.

---

## Quick Reference

**Admin Panel URL:**
```
https://your-app-name.onrender.com/admin.html
```

**Create Admin (Render Shell):**
```python
python
from backend.app import app, db
from backend.models import User
with app.app_context():
    admin = User(username='admin', email='admin@example.com')
    admin.set_password('YourPassword123')
    admin.is_admin = True
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin created!")
```

**Make User Admin (Render Shell):**
```python
python
from backend.app import app, db
from backend.models import User
with app.app_context():
    user = User.query.filter_by(username='your_username').first()
    user.is_admin = True
    db.session.commit()
    print("✅ User is now admin!")
```

---

**Made with Bob** 🤖