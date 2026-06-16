# 🏗️ Architecture Documentation

## System Overview

The World Cup 2026 Predictor is a full-stack web application built with a Python Flask backend and vanilla JavaScript frontend.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (HTML/JS)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │  Login   │  │ Matches  │  │Predictions│  │Leaderboard││
│  │  Page    │  │   View   │  │   View    │  │  View   ││
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘│
│                         │                                │
│                    app.js (API Client)                   │
└─────────────────────────┼───────────────────────────────┘
                          │ HTTP/REST API
                          │
┌─────────────────────────▼───────────────────────────────┐
│                  Backend (Flask)                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              app.py (Main Application)            │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐ │  │
│  │  │   Auth     │  │  Matches   │  │Predictions │ │  │
│  │  │  Routes    │  │   Routes   │  │  Routes    │ │  │
│  │  └────────────┘  └────────────┘  └────────────┘ │  │
│  │  ┌────────────┐                                  │  │
│  │  │Leaderboard │                                  │  │
│  │  │  Routes    │                                  │  │
│  │  └────────────┘                                  │  │
│  └──────────────────────┼───────────────────────────┘  │
│                         │                               │
│  ┌──────────────────────▼───────────────────────────┐  │
│  │           models.py (Data Models)                 │  │
│  │  ┌──────┐  ┌──────┐  ┌──────────┐               │  │
│  │  │ User │  │Match │  │Prediction│               │  │
│  │  └──────┘  └──────┘  └──────────┘               │  │
│  └──────────────────────┼───────────────────────────┘  │
└─────────────────────────┼───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│              Database (SQLite/PostgreSQL)                │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐         │
│  │  users   │  │ matches  │  │ predictions  │         │
│  └──────────┘  └──────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────┘
```

## Technology Stack

### Backend
- **Framework**: Flask 3.0
- **ORM**: Flask-SQLAlchemy
- **Authentication**: Flask-Login
- **CORS**: Flask-CORS
- **Database**: SQLite (development), PostgreSQL (production)
- **Server**: Gunicorn (production)

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling with gradients and animations
- **Vanilla JavaScript**: No frameworks for simplicity
- **Fetch API**: HTTP requests to backend

## Database Schema

### Users Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Matches Table
```sql
CREATE TABLE match (
    id INTEGER PRIMARY KEY,
    team_home VARCHAR(100) NOT NULL,
    team_away VARCHAR(100) NOT NULL,
    match_date DATETIME NOT NULL,
    stage VARCHAR(50) NOT NULL,
    home_score INTEGER,
    away_score INTEGER,
    is_finished BOOLEAN DEFAULT FALSE
);
```

### Predictions Table
```sql
CREATE TABLE prediction (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    match_id INTEGER NOT NULL,
    predicted_home_score INTEGER NOT NULL,
    predicted_away_score INTEGER NOT NULL,
    predicted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    points_earned INTEGER,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (match_id) REFERENCES match(id),
    UNIQUE (user_id, match_id)
);
```

## API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/register` | Register new user | No |
| POST | `/api/login` | Login user | No |
| POST | `/api/logout` | Logout user | Yes |
| GET | `/api/current-user` | Get current user info | Yes |

### Match Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/matches` | Get all matches | No |
| GET | `/api/matches/<id>` | Get specific match | No |
| POST | `/api/matches` | Create new match | Yes (Admin) |
| PUT | `/api/matches/<id>/result` | Update match result | Yes (Admin) |

### Prediction Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/predictions` | Create/update prediction | Yes |
| GET | `/api/predictions/my` | Get user's predictions | Yes |
| GET | `/api/predictions/match/<id>` | Get match predictions | Yes |

### Leaderboard Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/leaderboard` | Get rankings | No |

## Data Flow

### User Registration Flow
```
User → Frontend Form → POST /api/register → Backend Validation
→ Hash Password → Save to Database → Return Success
```

### Prediction Submission Flow
```
User → Select Match → Enter Scores → POST /api/predictions
→ Validate (match not started) → Check existing prediction
→ Create/Update prediction → Save to Database → Return Success
```

### Points Calculation Flow
```
Admin → Update Match Result → PUT /api/matches/<id>/result
→ Update match scores → Set is_finished = True
→ For each prediction:
    - Compare predicted vs actual scores
    - Exact match: 3 points
    - Correct winner: 1 point
    - Wrong: 0 points
→ Update prediction.points_earned → Commit to Database
```

### Leaderboard Generation Flow
```
Request → GET /api/leaderboard → Query all users
→ For each user:
    - Calculate total points
    - Count correct winners
    - Count exact scores
→ Sort by total points (descending) → Return ranked list
```

## Security Considerations

### Implemented
- ✅ Password hashing with Werkzeug
- ✅ Session-based authentication with Flask-Login
- ✅ CORS configuration
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Input validation

### Recommended for Production
- 🔒 HTTPS/SSL encryption
- 🔒 Rate limiting
- 🔒 CSRF protection
- 🔒 Environment variable management
- 🔒 Database backups
- 🔒 Admin role-based access control

## Scalability Considerations

### Current Design (Small Groups)
- SQLite database (file-based)
- Single server deployment
- Session-based authentication
- Suitable for: 5-50 users

### For Larger Scale
1. **Database**: Migrate to PostgreSQL
2. **Caching**: Add Redis for sessions and leaderboard
3. **Load Balancing**: Multiple backend instances
4. **CDN**: Serve static frontend files
5. **WebSockets**: Real-time updates
6. **Microservices**: Separate prediction and leaderboard services

## Extension Points

### Easy to Add
1. **Admin Panel**: Create admin routes and UI
2. **Email Notifications**: Add Flask-Mail
3. **Social Features**: Add comments table and routes
4. **Statistics**: Add analytics endpoints
5. **Mobile App**: Use existing API

### Moderate Complexity
1. **Real-time Updates**: Add WebSocket support
2. **Group Competitions**: Add groups table
3. **Betting System**: Add virtual currency
4. **Social Login**: OAuth integration
5. **Push Notifications**: Add service worker

### Advanced Features
1. **Machine Learning**: Predict match outcomes
2. **Live Scores**: Integrate with sports API
3. **Video Highlights**: Embed match videos
4. **Chat System**: Real-time messaging
5. **Mobile Apps**: Native iOS/Android

## File Structure

```
worldcup-predictor/
├── backend/
│   ├── __init__.py          # Package initialization
│   ├── app.py               # Main Flask application
│   ├── models.py            # Database models
│   └── seed_data.py         # Data seeding script
├── frontend/
│   ├── index.html           # Main HTML page
│   └── app.js               # Frontend JavaScript
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
├── Procfile                # Heroku deployment
├── README.md               # User documentation
├── SETUP_GUIDE.md          # Quick setup guide
└── ARCHITECTURE.md         # This file
```

## Development Workflow

1. **Local Development**
   - Use SQLite database
   - Flask debug mode enabled
   - CORS allows all origins

2. **Testing**
   - Manual testing via frontend
   - API testing with curl/Postman
   - (Future: Add unit tests)

3. **Deployment**
   - Switch to PostgreSQL
   - Disable debug mode
   - Configure CORS for specific domain
   - Use gunicorn server
   - Set secure SECRET_KEY

## Performance Optimization

### Current Implementation
- Database queries optimized with relationships
- Leaderboard calculated on-demand
- Frontend caches user data

### Future Optimizations
- Cache leaderboard (Redis)
- Paginate match lists
- Lazy load predictions
- Compress API responses
- Add database indexes

## Monitoring & Maintenance

### Recommended Tools
- **Logging**: Python logging module
- **Error Tracking**: Sentry
- **Analytics**: Google Analytics
- **Uptime**: UptimeRobot
- **Database**: Regular backups

### Maintenance Tasks
- Weekly database backups
- Monitor disk space
- Review error logs
- Update dependencies
- Clean old sessions

---

**This architecture is designed to be simple, maintainable, and extensible for a small group of friends while allowing for future growth.**