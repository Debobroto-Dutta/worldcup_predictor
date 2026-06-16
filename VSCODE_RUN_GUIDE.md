# 🚀 VSCode Step-by-Step Run Guide

## Prerequisites Check
Before starting, ensure you have:
- ✅ Python 3.8+ installed
- ✅ VSCode installed
- ✅ Terminal access in VSCode

---

## 📋 Step-by-Step Instructions

### Step 1: Open Project in VSCode
1. Open VSCode
2. Click **File** → **Open Folder**
3. Navigate to and select the `worldcup-predictor` folder
4. Click **Select Folder**

### Step 2: Open Integrated Terminal
1. In VSCode, press **Ctrl + `** (backtick) or
2. Go to **View** → **Terminal**
3. A terminal will open at the bottom of VSCode

### Step 3: Verify Virtual Environment
The project already has a virtual environment (`venv`). Verify it exists:
```bash
ls -la venv/
```

If you see the `venv` folder, proceed to Step 4.

### Step 4: Activate Virtual Environment
In the VSCode terminal, run:

**For Linux/Mac:**
```bash
source venv/bin/activate
```

**For Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` appear at the start of your terminal prompt.

### Step 5: Verify Dependencies
Check if all packages are installed:
```bash
pip list
```

If Flask is missing, install dependencies:
```bash
pip install -r requirements.txt
```

### Step 6: Initialize Database (First Time Only)
If this is your first time running the project:
```bash
cd backend
python init_db.py
cd ..
```

You should see: ✅ Database initialized successfully with is_admin column!

### Step 7: (Optional) Add Sample Data
To populate the database with sample matches:
```bash
cd backend
python seed_data.py
cd ..
```

### Step 8: Start the Backend Server
```bash
cd backend
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Running on http://9.22.209.107:5000
```

**✅ Backend is now running!** Keep this terminal open.

### Step 9: Open Frontend in Browser

**Option A: Using VSCode Live Server Extension (Recommended)**
1. Install "Live Server" extension in VSCode if not already installed
2. Right-click on `frontend/index.html`
3. Select **Open with Live Server**
4. Browser will open automatically

**Option B: Direct File Access**
1. Open a new terminal in VSCode (**Terminal** → **New Terminal**)
2. Run:
   ```bash
   xdg-open frontend/index.html
   ```
   Or manually open: `file:///home/debobrod/Desktop/worldcup-predictor/frontend/index.html`

### Step 10: Test the Application

#### In the Browser (Frontend):
1. You should see the World Cup Predictor homepage
2. Click **Register** to create a new account
3. Fill in:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `password123`
4. Click **Register**
5. Login with your credentials
6. Explore the features:
   - View matches
   - Make predictions
   - Check leaderboard

#### Test Backend API:
Open a new browser tab and visit:
- http://127.0.0.1:5000/ - API information
- http://127.0.0.1:5000/api/health - Health check
- http://127.0.0.1:5000/api/leaderboard - View leaderboard

---

## 🎯 Quick Start Commands (All-in-One)

Open VSCode terminal and run these commands in sequence:

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Go to backend directory
cd backend

# 3. Initialize database (first time only)
python init_db.py

# 4. (Optional) Add sample data
python seed_data.py

# 5. Start the server
python app.py
```

Then open `frontend/index.html` in your browser.

---

## 🛑 How to Stop

### Stop Backend Server:
- In the terminal running `python app.py`, press **Ctrl + C**

### Close Frontend:
- Simply close the browser tab

---

## 📁 Project Structure
```
worldcup-predictor/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── models.py           # Database models
│   ├── init_db.py          # Database initialization
│   ├── seed_data.py        # Sample data script
│   └── instance/
│       └── worldcup.db     # SQLite database
├── frontend/
│   ├── index.html          # Main page
│   ├── admin.html          # Admin panel
│   └── reset-password.html # Password reset
├── venv/                   # Virtual environment
└── requirements.txt        # Python dependencies
```

---

## 🔧 Troubleshooting

### Issue: "python: command not found"
**Solution:** Use `python3` instead:
```bash
python3 app.py
```

### Issue: "No module named 'flask'"
**Solution:** Activate virtual environment and install dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Database error" or "no such column"
**Solution:** Reinitialize the database:
```bash
cd backend
rm -rf instance/
python init_db.py
```

### Issue: Frontend can't connect to backend
**Solution:** 
1. Ensure backend is running on http://127.0.0.1:5000
2. Check browser console for CORS errors
3. Verify the API URL in frontend JavaScript files

### Issue: Port 5000 already in use
**Solution:** Kill the process using port 5000:
```bash
lsof -ti:5000 | xargs kill -9
```

---

## 🎨 VSCode Extensions (Recommended)

Install these extensions for better development experience:
1. **Python** (Microsoft) - Python language support
2. **Live Server** (Ritwick Dey) - Launch frontend with live reload
3. **SQLite Viewer** - View database contents
4. **REST Client** - Test API endpoints

---

## 📝 Next Steps

1. ✅ Create a user account
2. ✅ Add some match predictions
3. ✅ Check the leaderboard
4. ✅ Try the admin panel (create admin user first)
5. ✅ Test password reset functionality

---

## 🆘 Need Help?

- Check `README.md` for project overview
- Check `SETUP_GUIDE.md` for detailed setup
- Check `ADMIN_SETUP.md` for admin features
- Check terminal output for error messages

---

**Made with Bob** 🤖