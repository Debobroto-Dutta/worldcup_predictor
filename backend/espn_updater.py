"""
ESPN API Integration for Live Cricket Scores
Fetches live match results from ESPN Cricinfo API
Updates every 60 minutes
"""
import requests
from datetime import datetime
from backend.models import db, Match, Prediction


class ESPNUpdater:
    """Handles automatic match result updates from ESPN API"""
    
    def __init__(self, app=None):
        self.app = app
        # ESPN Cricinfo API endpoints
        self.base_url = "https://hs-consumer-api.espncricinfo.com/v1/pages"
        
    def fetch_live_matches(self):
        """
        Fetch live cricket matches from ESPN API
        
        Returns:
            List of live match data from ESPN
        """
        try:
            # ESPN API endpoint for live matches
            url = f"{self.base_url}/matches/current"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            matches = data.get('matches', [])
            
            return matches if isinstance(matches, list) else []
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching matches from ESPN API: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []
    
    def fetch_match_details(self, match_id):
        """
        Fetch detailed match information from ESPN API
        
        Args:
            match_id: ESPN match ID
            
        Returns:
            Match details dictionary
        """
        try:
            url = f"{self.base_url}/match/details?matchId={match_id}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"❌ Error fetching match details: {e}")
            return None
    
    def update_match_from_espn(self, match_data):
        """
        Update a single match from ESPN data
        
        Args:
            match_data: ESPN match data dictionary
            
        Returns:
            Boolean indicating if match was updated
        """
        if not self.app:
            return False
        
        with self.app.app_context():
            try:
                # Extract match information
                espn_id = str(match_data.get('objectId', ''))
                teams = match_data.get('teams', [])
                
                if len(teams) < 2:
                    return False
                
                team1 = teams[0].get('team', {}).get('name', '')
                team2 = teams[1].get('team', {}).get('name', '')
                
                # Get scores
                team1_score = teams[0].get('score', '')
                team2_score = teams[1].get('score', '')
                
                # Parse scores (format: "123/4" or "123")
                def parse_score(score_str):
                    if not score_str or score_str == '-':
                        return None
                    try:
                        # Extract runs (before '/')
                        return int(score_str.split('/')[0])
                    except:
                        return None
                
                score1 = parse_score(team1_score)
                score2 = parse_score(team2_score)
                
                # Check match status
                status = match_data.get('status', '').lower()
                is_finished = status in ['complete', 'completed', 'result']
                
                # Find matching match in database by ESPN ID or team names
                match = None
                if espn_id:
                    match = Match.query.filter_by(espn_match_id=espn_id).first()
                
                if not match:
                    # Try to find by team names
                    match = Match.query.filter(
                        db.or_(
                            db.and_(
                                Match.team_home.ilike(f'%{team1}%'),
                                Match.team_away.ilike(f'%{team2}%')
                            ),
                            db.and_(
                                Match.team_home.ilike(f'%{team2}%'),
                                Match.team_away.ilike(f'%{team1}%')
                            )
                        )
                    ).first()
                
                if match:
                    # Update ESPN ID if not set
                    if not match.espn_match_id and espn_id:
                        match.espn_match_id = espn_id
                    
                    # Update scores if available
                    if score1 is not None and score2 is not None:
                        # Determine which team is home/away
                        if team1.lower() in match.team_home.lower():
                            match.home_score = score1
                            match.away_score = score2
                        else:
                            match.home_score = score2
                            match.away_score = score1
                    
                    # Update finished status
                    if is_finished and not match.is_finished:
                        match.is_finished = True
                        
                        # Calculate points for all predictions
                        for prediction in match.predictions:
                            prediction.points_earned = prediction.calculate_points()
                    
                    db.session.commit()
                    print(f"✅ Updated from ESPN: {team1} vs {team2}")
                    return True
                
                return False
                
            except Exception as e:
                print(f"❌ Error updating match from ESPN: {e}")
                db.session.rollback()
                return False
    
    def update_all_matches(self):
        """
        Update all matches from ESPN API
        
        Returns:
            Number of matches updated
        """
        if not self.app:
            print("⚠️  App context not available")
            return 0
        
        with self.app.app_context():
            try:
                live_matches = self.fetch_live_matches()
                
                if not live_matches:
                    print("ℹ️  No live matches found from ESPN")
                    return 0
                
                updated_count = 0
                
                for match_data in live_matches:
                    if self.update_match_from_espn(match_data):
                        updated_count += 1
                
                if updated_count > 0:
                    print(f"✅ Successfully updated {updated_count} match(es) from ESPN")
                else:
                    print("ℹ️  No matches needed updating from ESPN")
                
                return updated_count
                
            except Exception as e:
                print(f"❌ Error updating matches from ESPN: {e}")
                return 0
    
    def get_live_match_status(self):
        """
        Get current live match statuses
        
        Returns:
            List of live match information
        """
        try:
            live_matches = self.fetch_live_matches()
            
            result = []
            for match in live_matches:
                teams = match.get('teams', [])
                if len(teams) >= 2:
                    result.append({
                        'espn_id': match.get('objectId', ''),
                        'team1': teams[0].get('team', {}).get('name', ''),
                        'team2': teams[1].get('team', {}).get('name', ''),
                        'score1': teams[0].get('score', ''),
                        'score2': teams[1].get('score', ''),
                        'status': match.get('status', ''),
                        'stage': match.get('stage', {}).get('name', '')
                    })
            
            return result
            
        except Exception as e:
            print(f"❌ Error fetching live match status: {e}")
            return []


def setup_espn_scheduler(app):
    """
    Set up APScheduler to automatically fetch match results from ESPN every 60 minutes
    
    Args:
        app: Flask application instance
    """
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.interval import IntervalTrigger
    
    updater = ESPNUpdater(app)
    
    scheduler = BackgroundScheduler()
    
    # Run every 60 minutes
    scheduler.add_job(
        func=updater.update_all_matches,
        trigger=IntervalTrigger(minutes=60),
        id='espn_match_updater',
        name='Update match results from ESPN API every 60 minutes',
        replace_existing=True
    )
    
    scheduler.start()
    print("✅ ESPN match result auto-updater started (runs every 60 minutes)")
    
    return scheduler


# Made with Bob