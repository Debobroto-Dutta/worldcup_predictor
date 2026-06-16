from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import pytz

db = SQLAlchemy()

def get_ist_now():
    """Get current time in IST"""
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)

class User(UserMixin, db.Model):
    """User model for authentication and tracking"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=get_ist_now)
    
    # Relationships
    predictions = db.relationship('Prediction', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def get_total_points(self):
        """Calculate total points for user"""
        return sum(p.points_earned for p in self.predictions if p.points_earned is not None)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Match(db.Model):
    """Match model for World Cup matches"""
    id = db.Column(db.Integer, primary_key=True)
    team_home = db.Column(db.String(100), nullable=False)
    team_away = db.Column(db.String(100), nullable=False)
    match_date = db.Column(db.DateTime, nullable=False)
    stage = db.Column(db.String(50), nullable=False)  # Group, Round of 16, Quarter, Semi, Final
    
    # Actual results (null until match is played)
    home_score = db.Column(db.Integer, nullable=True)
    away_score = db.Column(db.Integer, nullable=True)
    is_finished = db.Column(db.Boolean, default=False)
    
    # Live streaming URL
    live_stream_url = db.Column(db.String(500), nullable=True)
    
    # ESPN API match ID for tracking
    espn_match_id = db.Column(db.String(100), nullable=True)
    
    # Relationships
    predictions = db.relationship('Prediction', backref='match', lazy=True, cascade='all, delete-orphan')
    
    def get_winner(self):
        """Get the winner of the match"""
        if not self.is_finished or self.home_score is None or self.away_score is None:
            return None
        if self.home_score > self.away_score:
            return 'home'
        elif self.away_score > self.home_score:
            return 'away'
        return 'draw'
    
    def __repr__(self):
        return f'<Match {self.team_home} vs {self.team_away}>'


class Prediction(db.Model):
    """Prediction model for user predictions"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    
    # User's prediction
    predicted_home_score = db.Column(db.Integer, nullable=False)
    predicted_away_score = db.Column(db.Integer, nullable=False)
    predicted_at = db.Column(db.DateTime, default=get_ist_now)
    
    # Points earned (calculated after match finishes)
    points_earned = db.Column(db.Integer, nullable=True)
    
    # Unique constraint: one prediction per user per match
    __table_args__ = (db.UniqueConstraint('user_id', 'match_id', name='_user_match_uc'),)
    
    def get_predicted_winner(self):
        """Get predicted winner"""
        if self.predicted_home_score > self.predicted_away_score:
            return 'home'
        elif self.predicted_away_score > self.predicted_home_score:
            return 'away'
        return 'draw'
    
    def calculate_points(self):
        """
        Calculate points based on prediction accuracy
        - Exact scoreline: 3 points
        - Correct winner only: 1 point
        - Wrong prediction: 0 points
        """
        if not self.match.is_finished:
            return None
        
        # Check for exact scoreline match
        if (self.predicted_home_score == self.match.home_score and 
            self.predicted_away_score == self.match.away_score):
            return 3
        
        # Check for correct winner
        predicted_winner = self.get_predicted_winner()
        actual_winner = self.match.get_winner()
        
        if predicted_winner == actual_winner:
            return 1
        
        return 0
    
    def __repr__(self):
        return f'<Prediction {self.user.username} - {self.match.team_home} vs {self.match.team_away}>'

# Made with Bob
