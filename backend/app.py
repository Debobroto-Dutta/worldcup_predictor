from flask import Flask, jsonify, request, url_for, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from backend.models import db, User, Match, Prediction
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Fix PostgreSQL URL for Render (postgres:// -> postgresql://)
database_url = os.environ.get('DATABASE_URL', 'sqlite:///worldcup.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session Configuration for production
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

# Email Configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@worldcuppredictor.com')

# Initialize extensions
db.init_app(app)
# CORS configuration - allow credentials and specify origin
CORS(app,
     supports_credentials=True,
     origins=['*'],  # In production, replace with your actual domain
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
mail = Mail(app)

# Token serializer for password reset
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============= Authentication Routes =============

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create new user
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {'id': user.id, 'username': user.username, 'email': user.email}
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    login_user(user)
    
    return jsonify({
        'message': 'Login successful',
        'user': {'id': user.id, 'username': user.username, 'email': user.email}
    }), 200

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """Logout user"""
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/current-user', methods=['GET'])
@login_required
def get_current_user():
    """Get current logged-in user"""
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'is_admin': current_user.is_admin,
        'total_points': current_user.get_total_points()
    }), 200
# ============= User Management Routes (Admin Only) =============

@app.route('/api/admin/users', methods=['GET'])
@login_required
def get_all_users():
    """Get all users with details (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    users = User.query.all()
    
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'total_points': user.get_total_points(),
        'predictions_count': len(user.predictions),
        'created_at': user.created_at.isoformat() if user.created_at else None
    } for user in users]), 200

@app.route('/api/admin/users/<int:user_id>', methods=['GET'])
@login_required
def get_user_details(user_id):
    """Get specific user details (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'total_points': user.get_total_points(),
        'predictions_count': len(user.predictions),
        'created_at': user.created_at.isoformat() if user.created_at else None,
        'predictions': [{
            'match_id': p.match_id,
            'team_home': p.match.team_home,
            'team_away': p.match.team_away,
            'predicted_home_score': p.predicted_home_score,
            'predicted_away_score': p.predicted_away_score,
            'points_earned': p.points_earned
        } for p in user.predictions]
    }), 200

@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    """Update user details (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    # Prevent admin from removing their own admin status
    if user.id == current_user.id and 'is_admin' in data and not data['is_admin']:
        return jsonify({'error': 'Cannot remove your own admin status'}), 400
    
    if 'username' in data:
        # Check if username is already taken by another user
        existing = User.query.filter_by(username=data['username']).first()
        if existing and existing.id != user_id:
            return jsonify({'error': 'Username already exists'}), 400
        user.username = data['username']
    
    if 'email' in data:
        # Check if email is already taken by another user
        existing = User.query.filter_by(email=data['email']).first()
        if existing and existing.id != user_id:
            return jsonify({'error': 'Email already exists'}), 400
        user.email = data['email']
    
    if 'is_admin' in data:
        user.is_admin = data['is_admin']
    
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    
    db.session.commit()
    
    return jsonify({'message': 'User updated successfully'}), 200

@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    """Delete a user (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    # Prevent admin from deleting themselves
    if user_id == current_user.id:
        return jsonify({'error': 'Cannot delete your own account'}), 400
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/api/admin/users/<int:user_id>/send-reset-email', methods=['POST'])
@login_required
def send_password_reset_email(user_id):
    """Send password reset email to user (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    user = User.query.get_or_404(user_id)
    
    # Generate password reset token (valid for 1 hour)
    token = serializer.dumps(user.email, salt='password-reset-salt')
    
    # Create reset link
    reset_url = f"{request.host_url}reset-password?token={token}"
    
    # Send email
    try:
        msg = Message(
            subject='Password Reset - World Cup Predictor',
            recipients=[user.email],
            body=f'''Hello {user.username},

An administrator has initiated a password reset for your World Cup Predictor account.

Click the link below to reset your password:
{reset_url}

This link will expire in 1 hour.

If you did not request this password reset, please ignore this email.

Best regards,
World Cup Predictor Team
''',
            html=f'''
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #667eea;">Password Reset Request</h2>
        <p>Hello <strong>{user.username}</strong>,</p>
        <p>An administrator has initiated a password reset for your World Cup Predictor account.</p>
        <p>Click the button below to reset your password:</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{reset_url}"
               style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                      color: white;
                      padding: 12px 30px;
                      text-decoration: none;
                      border-radius: 5px;
                      display: inline-block;">
                Reset Password
            </a>
        </div>
        <p style="color: #666; font-size: 14px;">
            This link will expire in 1 hour.
        </p>
        <p style="color: #666; font-size: 14px;">
            If you did not request this password reset, please ignore this email.
        </p>
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
        <p style="color: #999; font-size: 12px;">
            World Cup Predictor Team
        </p>
    </div>
</body>
</html>
'''
        )
        mail.send(msg)
        return jsonify({'message': f'Password reset email sent to {user.email}'}), 200
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({'error': 'Failed to send email. Please check email configuration.'}), 500

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    """Reset password using token from email"""
    data = request.get_json()
    
    if not data or not data.get('token') or not data.get('new_password'):
        return jsonify({'error': 'Token and new password required'}), 400
    
    try:
        # Verify token (valid for 1 hour = 3600 seconds)
        email = serializer.loads(data['token'], salt='password-reset-salt', max_age=3600)
        
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Update password
        user.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({'message': 'Password reset successfully'}), 200
        
    except SignatureExpired:
        return jsonify({'error': 'Reset link has expired. Please request a new one.'}), 400
    except BadSignature:
        return jsonify({'error': 'Invalid reset link'}), 400
    except Exception as e:
        print(f"Error resetting password: {e}")
        return jsonify({'error': 'Failed to reset password'}), 500

@app.route('/api/verify-reset-token', methods=['POST'])
def verify_reset_token():
    """Verify if a reset token is valid"""
    data = request.get_json()
    
    if not data or not data.get('token'):
        return jsonify({'error': 'Token required'}), 400
    
    try:
        email = serializer.loads(data['token'], salt='password-reset-salt', max_age=3600)
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({'error': 'Invalid token'}), 400
        
        return jsonify({
            'valid': True,
            'username': user.username,
            'email': user.email
        }), 200
        
    except SignatureExpired:
        return jsonify({'error': 'Token has expired'}), 400
    except BadSignature:
        return jsonify({'error': 'Invalid token'}), 400


# ============= Match Routes =============

@app.route('/api/matches', methods=['GET'])
def get_matches():
    """Get all matches"""
    matches = Match.query.order_by(Match.match_date).all()
    
    return jsonify([{
        'id': m.id,
        'team_home': m.team_home,
        'team_away': m.team_away,
        'match_date': m.match_date.isoformat(),
        'stage': m.stage,
        'home_score': m.home_score,
        'away_score': m.away_score,
        'is_finished': m.is_finished
    } for m in matches]), 200

@app.route('/api/matches/<int:match_id>', methods=['GET'])
def get_match(match_id):
    """Get a specific match"""
    match = Match.query.get_or_404(match_id)
    
    return jsonify({
        'id': match.id,
        'team_home': match.team_home,
        'team_away': match.team_away,
        'match_date': match.match_date.isoformat(),
        'stage': match.stage,
        'home_score': match.home_score,
        'away_score': match.away_score,
        'is_finished': match.is_finished
    }), 200

@app.route('/api/matches', methods=['POST'])
@login_required
def create_match():
    """Create a new match (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    data = request.get_json()
    
    if not all(k in data for k in ['team_home', 'team_away', 'match_date', 'stage']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    match = Match(
        team_home=data['team_home'],
        team_away=data['team_away'],
        match_date=datetime.fromisoformat(data['match_date']),
        stage=data['stage']
    )
    
    db.session.add(match)
    db.session.commit()
    
    return jsonify({
        'message': 'Match created successfully',
        'match_id': match.id
    }), 201

@app.route('/api/matches/<int:match_id>', methods=['PUT'])
@login_required
def update_match(match_id):
    """Update match details (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    match = Match.query.get_or_404(match_id)
    data = request.get_json()
    
    if 'team_home' in data:
        match.team_home = data['team_home']
    if 'team_away' in data:
        match.team_away = data['team_away']
    if 'match_date' in data:
        match.match_date = datetime.fromisoformat(data['match_date'])
    if 'stage' in data:
        match.stage = data['stage']
    
    db.session.commit()
    
    return jsonify({'message': 'Match updated successfully'}), 200

@app.route('/api/matches/<int:match_id>', methods=['DELETE'])
@login_required
def delete_match(match_id):
    """Delete a match (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    match = Match.query.get_or_404(match_id)
    db.session.delete(match)
    db.session.commit()
    
    return jsonify({'message': 'Match deleted successfully'}), 200

@app.route('/api/matches/<int:match_id>/result', methods=['PUT'])
@login_required
def update_match_result(match_id):
    """Update match result and calculate points (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    match = Match.query.get_or_404(match_id)
    data = request.get_json()
    
    if not all(k in data for k in ['home_score', 'away_score']):
        return jsonify({'error': 'Missing score data'}), 400
    
    match.home_score = data['home_score']
    match.away_score = data['away_score']
    match.is_finished = True
    
    # Calculate points for all predictions
    for prediction in match.predictions:
        prediction.points_earned = prediction.calculate_points()
    
    db.session.commit()
    
    return jsonify({'message': 'Match result updated and points calculated'}), 200

# ============= Prediction Routes =============

@app.route('/api/predictions', methods=['POST'])
@login_required
def create_prediction():
    """Create or update a prediction"""
    data = request.get_json()
    
    if not all(k in data for k in ['match_id', 'predicted_home_score', 'predicted_away_score']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    match = Match.query.get_or_404(data['match_id'])
    
    # Check if match has already started
    if match.match_date < datetime.utcnow():
        return jsonify({'error': 'Cannot predict for matches that have already started'}), 400
    
    # Check if prediction already exists
    prediction = Prediction.query.filter_by(
        user_id=current_user.id,
        match_id=data['match_id']
    ).first()
    
    if prediction:
        # Update existing prediction
        prediction.predicted_home_score = data['predicted_home_score']
        prediction.predicted_away_score = data['predicted_away_score']
        prediction.predicted_at = datetime.utcnow()
        message = 'Prediction updated successfully'
    else:
        # Create new prediction
        prediction = Prediction(
            user_id=current_user.id,
            match_id=data['match_id'],
            predicted_home_score=data['predicted_home_score'],
            predicted_away_score=data['predicted_away_score']
        )
        db.session.add(prediction)
        message = 'Prediction created successfully'
    
    db.session.commit()
    
    return jsonify({
        'message': message,
        'prediction_id': prediction.id
    }), 201

@app.route('/api/predictions/my', methods=['GET'])
@login_required
def get_my_predictions():
    """Get current user's predictions"""
    predictions = Prediction.query.filter_by(user_id=current_user.id).all()
    
    return jsonify([{
        'id': p.id,
        'match_id': p.match_id,
        'team_home': p.match.team_home,
        'team_away': p.match.team_away,
        'predicted_home_score': p.predicted_home_score,
        'predicted_away_score': p.predicted_away_score,
        'points_earned': p.points_earned,
        'match_finished': p.match.is_finished
    } for p in predictions]), 200

@app.route('/api/predictions/match/<int:match_id>', methods=['GET'])
@login_required
def get_match_predictions(match_id):
    """Get all predictions for a specific match (only show after match starts)"""
    match = Match.query.get_or_404(match_id)
    
    # Only show predictions after match has started
    if match.match_date > datetime.utcnow():
        return jsonify({'error': 'Predictions not visible until match starts'}), 403
    
    predictions = Prediction.query.filter_by(match_id=match_id).all()
    
    return jsonify([{
        'username': p.user.username,
        'predicted_home_score': p.predicted_home_score,
        'predicted_away_score': p.predicted_away_score,
        'points_earned': p.points_earned
    } for p in predictions]), 200

# ============= Leaderboard Routes =============

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get leaderboard with all users and their points"""
    users = User.query.all()
    
    leaderboard = []
    for user in users:
        total_points = user.get_total_points()
        correct_winners = sum(1 for p in user.predictions if p.points_earned and p.points_earned >= 1)
        exact_scores = sum(1 for p in user.predictions if p.points_earned == 3)
        
        leaderboard.append({
            'username': user.username,
            'total_points': total_points,
            'correct_winners': correct_winners,
            'exact_scores': exact_scores,
            'predictions_made': len(user.predictions)
        })
    
    # Sort by total points (descending)
    leaderboard.sort(key=lambda x: x['total_points'], reverse=True)
    
    # Add rank
    for i, entry in enumerate(leaderboard, 1):
        entry['rank'] = i
    
    return jsonify(leaderboard), 200

# ============= Database Initialization =============

@app.route('/api/init-db', methods=['POST'])
def init_database():
    """Initialize database (use only once)"""
    db.create_all()
    return jsonify({'message': 'Database initialized successfully'}), 200

# ============= Root Route =============

@app.route('/')
def index():
    """Serve the main frontend page"""
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')
    return send_from_directory(frontend_dir, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static frontend files"""
    # Check if it's an API route
    if path.startswith('api/'):
        return jsonify({'error': 'API endpoint not found'}), 404
    
    # Serve frontend files
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')
    try:
        return send_from_directory(frontend_dir, path)
    except:
        # If file not found, return index.html for SPA routing
        return send_from_directory(frontend_dir, 'index.html')

@app.route('/api')
def api_info():
    """API information endpoint"""
    return jsonify({
        'name': 'World Cup 2026 Predictor API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'auth': ['/api/register', '/api/login', '/api/logout'],
            'user': ['/api/user', '/api/request-password-reset', '/api/reset-password/<token>'],
            'matches': ['/api/matches', '/api/matches/<id>'],
            'predictions': ['/api/predictions', '/api/predictions/<id>'],
            'leaderboard': ['/api/leaderboard'],
            'admin': ['/api/admin/matches', '/api/admin/matches/<id>', '/api/admin/users', '/api/admin/calculate-points'],
            'health': ['/api/health']
        },
        'documentation': 'See README.md for full API documentation'
    }), 200

# ============= Health Check =============

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

@app.route('/api/admin/backfill-results', methods=['POST'])
@login_required
def backfill_results():
    """Manually trigger backfill of all match results (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        from backend.match_updater import MatchUpdater
        updater = MatchUpdater(app)
        updated_count = updater.backfill_all_results()
        
        return jsonify({
            'message': f'Successfully backfilled {updated_count} match(es)',
            'updated_count': updated_count
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/test-api', methods=['GET'])
@login_required
def test_api():
    """Test the World Cup API connection (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        from backend.match_updater import MatchUpdater
        updater = MatchUpdater(app)
        matches = updater.fetch_world_cup_matches()
        
        return jsonify({
            'message': f'Found {len(matches)} matches from API',
            'matches_count': len(matches),
            'sample_matches': matches[:3] if matches else []
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/sync-matches', methods=['POST'])
@login_required
def sync_matches():
    """Sync all matches from API to database (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        from backend.match_updater import MatchUpdater
        updater = MatchUpdater(app)
        created, updated = updater.sync_matches_from_api()
        
        return jsonify({
            'message': f'Sync complete: {created} created, {updated} updated',
            'created_count': created,
            'updated_count': updated
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/live-scores', methods=['GET'])
def get_live_scores():
    """Get current live scores from API (public endpoint)"""
    try:
        from backend.match_updater import MatchUpdater
        updater = MatchUpdater(app)
        live_matches = updater.get_live_scores()
        
        return jsonify({
            'live_matches': live_matches,
            'count': len(live_matches)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teams', methods=['GET'])
def get_teams():
    """Get all teams from API (public endpoint)"""
    try:
        from backend.match_updater import MatchUpdater
        updater = MatchUpdater(app)
        teams_data = updater.fetch_teams()
        
        if teams_data:
            return jsonify(teams_data), 200
        else:
            return jsonify({'error': 'Failed to fetch teams'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Initialize database tables on startup (no data seeding)
with app.app_context():
    try:
        # Only create tables if they don't exist
        db.create_all()
        print("✓ Database tables checked/created")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")

# Initialize automatic match result updater
try:
    from backend.match_updater import setup_scheduler, MatchUpdater
    
    # First, backfill all historical results (matches already played)
    updater = MatchUpdater(app)
    backfilled = updater.backfill_all_results()
    if backfilled > 0:
        print(f"✓ Backfilled {backfilled} historical match result(s)")
    
    # Then start the scheduler for ongoing updates
    scheduler = setup_scheduler(app)
    print("✓ Automatic match result updater initialized")
except Exception as e:
    print(f"⚠️  Match updater initialization warning: {e}")
    print("   Manual result updates will still work via admin panel")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
