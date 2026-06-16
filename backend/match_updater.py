"""
Automatic Match Result Updater
Fetches live match results from World Cup 2026 API (Free, No Key Required!)
API Source: https://github.com/rezarahiminia/worldcup2026
"""
import requests
import os
from datetime import datetime
from backend.models import db, Match, Prediction

class MatchUpdater:
    """Handles automatic match result updates from external API"""
    
    def __init__(self, app=None):
        self.app = app
        # Free World Cup 2026 API - No API key required!
        self.base_url = "https://worldcupjson.net"
        
    def fetch_world_cup_matches(self):
        """
        Fetch World Cup 2026 matches from free API
        
        Returns:
            List of match data from API
        """
        try:
            # Fetch all matches
            url = f"{self.base_url}/matches"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            matches = response.json()
            return matches if isinstance(matches, list) else []
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching matches from API: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []
    
    def fetch_today_matches(self):
        """
        Fetch today's World Cup 2026 matches
        
        Returns:
            List of today's match data
        """
        try:
            url = f"{self.base_url}/matches/today"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            matches = response.json()
            return matches if isinstance(matches, list) else []
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching today's matches: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []
    
    def update_match_results(self, include_already_finished=False):
        """
        Update match results from API for finished matches
        
        Args:
            include_already_finished: If True, also update matches already marked as finished
        
        Returns:
            Number of matches updated
        """
        if not self.app:
            print("⚠️  App context not available")
            return 0
        
        with self.app.app_context():
            try:
                # Fetch all matches from API
                api_matches = self.fetch_world_cup_matches()
                
                if not api_matches:
                    print("ℹ️  No matches found from API")
                    return 0
                
                updated_count = 0
                
                for api_match in api_matches:
                    # Extract match data from World Cup 2026 API format
                    status = api_match.get('status', '')
                    
                    # Only process finished matches
                    if status not in ['completed', 'full-time']:
                        continue
                    
                    home_team = api_match.get('home_team', {}).get('name', '')
                    away_team = api_match.get('away_team', {}).get('name', '')
                    home_score = api_match.get('home_team', {}).get('goals')
                    away_score = api_match.get('away_team', {}).get('goals')
                    
                    if not all([home_team, away_team, home_score is not None, away_score is not None]):
                        continue
                    
                    # Find matching match in database
                    # If include_already_finished is True, update all matches, otherwise only unfinished ones
                    if include_already_finished:
                        match = Match.query.filter(
                            Match.team_home.ilike(f'%{home_team}%'),
                            Match.team_away.ilike(f'%{away_team}%')
                        ).first()
                    else:
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
    
    def backfill_all_results(self):
        """
        Backfill all historical match results (for matches already played)
        This will update ALL finished matches from the API, even if already marked as finished
        
        Returns:
            Number of matches updated
        """
        print("🔄 Starting backfill of all historical match results...")
        return self.update_match_results(include_already_finished=True)
    
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
