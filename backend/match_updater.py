"""
Automatic Match Result Updater
Fetches live match results from API-Football (free tier)
"""
import requests
import os
from datetime import datetime
from backend.models import db, Match, Prediction

class MatchUpdater:
    """Handles automatic match result updates from external API"""
    
    def __init__(self, app=None):
        self.app = app
        self.api_key = os.environ.get('FOOTBALL_API_KEY', '')
        self.api_host = "api-football-v1.p.rapidapi.com"
        self.base_url = f"https://{self.api_host}/v3"
        
    def get_headers(self):
        """Get API request headers"""
        return {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': self.api_host
        }
    
    def fetch_world_cup_matches(self, date=None):
        """
        Fetch World Cup 2026 matches from API
        
        Args:
            date: Date in YYYY-MM-DD format (optional)
        
        Returns:
            List of match data from API
        """
        if not self.api_key:
            print("⚠️  FOOTBALL_API_KEY not set. Skipping auto-update.")
            return []
        
        try:
            # World Cup 2026 league ID (will be available closer to tournament)
            # For now, using a placeholder - update when official ID is available
            league_id = 1  # FIFA World Cup
            season = 2026
            
            url = f"{self.base_url}/fixtures"
            params = {
                'league': league_id,
                'season': season
            }
            
            if date:
                params['date'] = date
            
            response = requests.get(url, headers=self.get_headers(), params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('response', [])
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching matches from API: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []
    
    def update_match_results(self):
        """
        Update match results from API for finished matches
        
        Returns:
            Number of matches updated
        """
        if not self.app:
            print("⚠️  App context not available")
            return 0
        
        with self.app.app_context():
            try:
                # Get today's date
                today = datetime.utcnow().strftime('%Y-%m-%d')
                
                # Fetch matches from API
                api_matches = self.fetch_world_cup_matches(date=today)
                
                if not api_matches:
                    print("ℹ️  No matches found from API")
                    return 0
                
                updated_count = 0
                
                for api_match in api_matches:
                    # Extract match data
                    fixture = api_match.get('fixture', {})
                    teams = api_match.get('teams', {})
                    goals = api_match.get('goals', {})
                    status = fixture.get('status', {}).get('short', '')
                    
                    # Only process finished matches
                    if status not in ['FT', 'AET', 'PEN']:
                        continue
                    
                    home_team = teams.get('home', {}).get('name', '')
                    away_team = teams.get('away', {}).get('name', '')
                    home_score = goals.get('home')
                    away_score = goals.get('away')
                    
                    if not all([home_team, away_team, home_score is not None, away_score is not None]):
                        continue
                    
                    # Find matching match in database
                    match = Match.query.filter(
                        Match.team_home.ilike(f'%{home_team}%'),
                        Match.team_away.ilike(f'%{away_team}%'),
                        Match.is_finished == False
                    ).first()
                    
                    if match:
                        # Update match result
                        match.home_score = home_score
                        match.away_score = away_score
                        match.is_finished = True
                        
                        # Calculate points for all predictions
                        for prediction in match.predictions:
                            prediction.points_earned = prediction.calculate_points()
                        
                        db.session.commit()
                        updated_count += 1
                        print(f"✅ Updated: {home_team} {home_score}-{away_score} {away_team}")
                
                if updated_count > 0:
                    print(f"✅ Successfully updated {updated_count} match(es)")
                else:
                    print("ℹ️  No matches needed updating")
                
                return updated_count
                
            except Exception as e:
                print(f"❌ Error updating match results: {e}")
                db.session.rollback()
                return 0
    
    def manual_update_match(self, match_id, home_score, away_score):
        """
        Manually update a specific match (fallback method)
        
        Args:
            match_id: Database match ID
            home_score: Home team score
            away_score: Away team score
        
        Returns:
            Boolean indicating success
        """
        if not self.app:
            return False
        
        with self.app.app_context():
            try:
                match = Match.query.get(match_id)
                if not match:
                    print(f"❌ Match {match_id} not found")
                    return False
                
                match.home_score = home_score
                match.away_score = away_score
                match.is_finished = True
                
                # Calculate points for all predictions
                for prediction in match.predictions:
                    prediction.points_earned = prediction.calculate_points()
                
                db.session.commit()
                print(f"✅ Manually updated match {match_id}")
                return True
                
            except Exception as e:
                print(f"❌ Error manually updating match: {e}")
                db.session.rollback()
                return False


def setup_scheduler(app):
    """
    Set up APScheduler to automatically fetch match results
    
    Args:
        app: Flask application instance
    """
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.interval import IntervalTrigger
    
    updater = MatchUpdater(app)
    
    scheduler = BackgroundScheduler()
    
    # Run every 15 minutes during tournament
    scheduler.add_job(
        func=updater.update_match_results,
        trigger=IntervalTrigger(minutes=15),
        id='match_updater',
        name='Update match results from API',
        replace_existing=True
    )
    
    scheduler.start()
    print("✅ Match result auto-updater started (runs every 15 minutes)")
    
    return scheduler

# Made with Bob
