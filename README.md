# ⚽ World Cup 2026 Predictor

A web application for friends to predict World Cup 2026 match winners and scorelines, compete on a leaderboard, and track points.

## 🎯 Features

- **User Authentication**: Register and login system for friends
- **Match Predictions**: Predict match winners and exact scorelines
- **Scoring System**:
  - 3 points for exact scoreline prediction
  - 1 point for correct winner prediction
  - 0 points for incorrect predictions
- **Leaderboard**: Real-time rankings showing top predictors
- **Live Football Scores**: Automatic integration with worldcupjson.net API
  - Real-time score updates every 15 minutes
  - Live match tracking
  - Automatic points calculation
- **Admin Panel**: Manage matches, users, and sync scores
- **Responsive Design**: Works on desktop and mobile devices
- **Extensible Architecture**: Easy to add new features

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A modern web browser

## 🚀 Step-by-Step Setup Guide

### Step 1: Clone or Download the Project

```bash
cd worldcup-predictor
```

### Step 2: Create a Virtual Environment

**On Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

```bash
cp .env.example .env
```

Edit the `.env` file and update the `SECRET_KEY`:
```
SECRET_KEY=your-random-secret-key-here
```

### Step 5: Initialize the Database

```bash
cd backend
python app.py
```

This will create the database file `worldcup.db` in the backend directory.

Press `Ctrl+C` to stop the server after it starts.

### Step 6: Seed Sample Match Data

```bash
python seed_data.py
```

This will populate the database with sample World Cup 2026 matches.

### Step 7: Start the Backend Server

```bash
python app.py
```

The backend API will be running at `http://localhost:5000`

### Step 8: Open the Frontend

Open a new terminal window and navigate to the frontend directory:

```bash
cd ../frontend
```

You can serve the frontend using Python's built-in HTTP server:

```bash
python -m http.server 8000
```

Or simply open `index.html` directly in your browser.

### Step 9: Access the Application

Open your browser and go to:
- Frontend: `http://localhost:8000` (or open `frontend/index.html`)
- Backend API: `http://localhost:5000/api/health`

## 👥 Usage Guide

### For Users:

1. **Register**: Create an account with username, email, and password
2. **Login**: Sign in with your credentials
3. **Make Predictions**: 
   - Go to "Matches" tab
   - Enter predicted scores for upcoming matches
   - Submit before match starts
4. **View Results**: Check "My Predictions" to see your predictions and points earned
5. **Check Leaderboard**: See how you rank against your friends

### For Admins:

To add match results and calculate points, use the API:

```bash
curl -X PUT http://localhost:5000/api/matches/1/result \
  -H "Content-Type: application/json" \
  -d '{"home_score": 2, "away_score": 1}'
```

Or create an admin interface (future enhancement).

## 📁 Project Structure

```
worldcup-predictor/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── models.py           # Database models
│   └── seed_data.py        # Sample data seeding script
├── frontend/
│   ├── index.html          # Main HTML page
│   └── app.js              # Frontend JavaScript
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore file
├── Procfile               # Deployment configuration
└── README.md              # This file
```

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `password_hash`: Hashed password
- `created_at`: Registration timestamp

### Matches Table
- `id`: Primary key
- `team_home`: Home team name
- `team_away`: Away team name
- `match_date`: Match date and time
- `stage`: Tournament stage (Group, Round of 16, etc.)
- `home_score`: Actual home score (null until finished)
- `away_score`: Actual away score (null until finished)
- `is_finished`: Match completion status

### Predictions Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `match_id`: Foreign key to Matches
- `predicted_home_score`: User's predicted home score
- `predicted_away_score`: User's predicted away score
- `predicted_at`: Prediction timestamp
- `points_earned`: Points awarded (calculated after match)

## 🔌 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user
- `POST /api/logout` - Logout user
- `GET /api/current-user` - Get current user info

### Matches
- `GET /api/matches` - Get all matches
- `GET /api/matches/<id>` - Get specific match
- `POST /api/matches` - Create new match (admin)
- `PUT /api/matches/<id>/result` - Update match result (admin)

### Predictions
- `POST /api/predictions` - Create/update prediction
- `GET /api/predictions/my` - Get user's predictions
- `GET /api/predictions/match/<id>` - Get all predictions for a match

### Leaderboard
- `GET /api/leaderboard` - Get leaderboard rankings

## 🌐 Deployment Options

### Option 1: Heroku

1. Install Heroku CLI
2. Create a Heroku app:
```bash
heroku create your-app-name
```

3. Add PostgreSQL addon:
```bash
heroku addons:create heroku-postgresql:mini
```

4. Set environment variables:
```bash
heroku config:set SECRET_KEY=your-secret-key
```

5. Deploy:
```bash
git push heroku main
```

6. Initialize database:
```bash
heroku run python backend/seed_data.py
```

### Option 2: PythonAnywhere

1. Upload files to PythonAnywhere
2. Create a virtual environment
3. Install dependencies
4. Configure WSGI file to point to `backend/app.py`
5. Set up static files mapping for frontend

### Option 3: DigitalOcean/AWS/VPS

1. Set up a Linux server
2. Install Python, pip, and nginx
3. Clone the repository
4. Set up gunicorn as a service
5. Configure nginx as reverse proxy
6. Set up SSL with Let's Encrypt

### Option 4: Local Network (For Small Groups)

1. Find your local IP address:
   - Linux/Mac: `ifconfig` or `ip addr`
   - Windows: `ipconfig`

2. Update `frontend/app.js` to use your IP:
```javascript
const API_BASE_URL = 'http://YOUR_LOCAL_IP:5000/api';
```

3. Start the backend:
```bash
python backend/app.py
```

4. Share the frontend URL with friends:
```
http://YOUR_LOCAL_IP:8000
```

## 🔧 Adding New Features

The application is designed to be extensible. Here are some ideas:

### 1. Add Admin Panel
Create an admin interface to:
- Add/edit matches
- Update match results
- Manage users

### 2. Add Email Notifications
Notify users when:
- Matches are about to start
- Results are posted
- They earn points

### 3. Add Social Features
- Comments on matches
- Share predictions with friends
- Group competitions

### 4. Add Statistics
- User prediction accuracy
- Most predicted teams
- Historical performance

### 5. Add Bonus Points
- Predict tournament winner
- Predict top scorer
- Daily/weekly challenges

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
rm backend/worldcup.db
cd backend
python app.py  # Creates new database
python seed_data.py  # Re-seed data
```

### CORS Issues
If you get CORS errors, ensure Flask-CORS is installed and configured in `app.py`.

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000  # Mac/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or use a different port
```

## 📝 License

This project is open source and available for personal use.

## 🤝 Contributing

Feel free to fork this project and add your own features!

## 📧 Support

For issues or questions, create an issue in the repository or contact the developer.

---

**Enjoy predicting the World Cup 2026! ⚽🏆**