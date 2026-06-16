# 🚀 Quick Setup Guide - World Cup 2026 Predictor

This is a simplified step-by-step guide to get your application running quickly.

## ⚡ Quick Start (5 Minutes)

### Step 1: Open Terminal in Project Directory
```bash
cd worldcup-predictor
```

### Step 2: Create Virtual Environment
```bash
# Linux/Mac
python3.8 -m venv venv  
#change as per version
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Requirements
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment
```bash
cp .env.example .env
```

### Step 5: Start Backend
```bash
cd backend
python3.8 app.py
```

Keep this terminal open. The backend is now running at `http://localhost:5000`

### Step 6: Open Frontend (New Terminal)
```bash
cd frontend
python3.8 -m http.server 8000
```

Or simply open `frontend/index.html` in your browser.

### Step 7: Access Application
Open browser: `http://localhost:8000`

### Step 8: Add Sample Data (Optional)
In the backend terminal (Ctrl+C to stop, then):
```bash
python3.8 seed_data.py
python3.8 app.py
```

## 🎮 First Time Usage

1. **Register**: Click "Register New Account"
   - Username: `admin`
   - Email: `debobroto.dutta@gmail.com`
   - Password: `1@3$5`

2. **Login**: Use your credentials

3. **Make Predictions**: Go to "Matches" tab and predict scores

4. **View Leaderboard**: Check rankings

## 🌐 Share with Friends

### Local Network (Same WiFi)

1. Find your IP address:
```bash
# Linux/Mac
ifconfig | grep "inet "

# Windows
ipconfig
```

2. Update `frontend/app.js` line 2:
```javascript
const API_BASE_URL = 'http://YOUR_IP_ADDRESS:5000/api';
```

3. Share with friends:
```
http://YOUR_IP_ADDRESS:8000
```

## 🔧 Common Issues

### "Port already in use"
```bash
# Use different port
python -m http.server 8080
```

### "Module not found"
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall
pip install -r requirements.txt
```

### "Database not found"
```bash
cd backend
python3.8 app.py  # This creates the database
```

## 📱 Adding Match Results (Admin)

Use curl or Postman:
```bash
curl -X PUT http://localhost:5000/api/matches/1/result \
  -H "Content-Type: application/json" \
  -d '{"home_score": 2, "away_score": 1}'
```

Or create a simple admin page (future enhancement).

## 🎯 Next Steps

1. ✅ Application is running
2. ✅ Users can register and login
3. ✅ Users can make predictions
4. ✅ Leaderboard is working

### To Deploy Online:
- See README.md for Heroku, PythonAnywhere, or VPS deployment
- For small groups, local network sharing is sufficient

## 💡 Tips

- **Backup Database**: Copy `backend/worldcup.db` regularly
- **Change Secret Key**: Update `.env` file with a secure random key
- **Add More Matches**: Edit `backend/seed_data.py` and run it again
- **Customize**: Modify `frontend/index.html` and `frontend/app.js` for your needs

## 🆘 Need Help?

Check the full README.md for:
- Detailed API documentation
- Deployment options
- Feature additions
- Troubleshooting

---

**You're all set! Start predicting! ⚽🏆**