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
        
        # Team name mapping: API country code -> Full team name
        self.team_mapping = {
            'QAT': 'Qatar', 'ECU': 'Ecuador', 'SEN': 'Senegal', 'NED': 'Netherlands',
            'ENG': 'England', 'IRN': 'Iran', 'USA': 'United States', 'WAL': 'Wales',
            'ARG': 'Argentina', 'KSA': 'Saudi Arabia', 'MEX': 'Mexico', 'POL': 'Poland',
            'FRA': 'France', 'AUS': 'Australia', 'DEN': 'Denmark', 'TUN': 'Tunisia',
            'ESP': 'Spain', 'CRC': 'Costa Rica', 'GER': 'Germany', 'JPN': 'Japan',
            'BEL': 'Belgium', 'CAN': 'Canada', 'MAR': 'Morocco', 'CRO': 'Croatia',
            'BRA': 'Brazil', 'SRB': 'Serbia', 'SUI': 'Switzerland', 'CMR': 'Cameroon',
            'POR': 'Portugal', 'GHA': 'Ghana', 'URU': 'Uruguay', 'KOR': 'South Korea'
        }
    
    def get_team_name(self, country_code):
        """
        Get full team name from country code
        
        Args:
            country_code: 3-letter country code (e.g., 'ENG', 'BRA')
        
        Returns:
            Full team name or country code if not found
        """
        return self.team_mapping.get(country_code, country_code)
    
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
    
    def fetch_teams(self):
        """
        Fetch all teams from the API
        
        Returns:
            Dictionary of teams organized by group
        """
        try:
            url = f"{self.base_url}/teams"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error fetching teams: {e}")
            return None
    
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
                    # FILTER: Only process 2026 matches, skip 2022 data
                    match_date_str = api_match.get('datetime', '')
                    if match_date_str and '2022' in match_date_str:
                        continue  # Skip 2022 World Cup matches
                    
                    # Extract match data from worldcupjson.net API format
                    status = api_match.get('status', '')
                    
                    # Only process finished matches
                    if status != 'completed':
                        continue
                    
                    # Get team names from the API response
                    home_team_data = api_match.get('home_team', {})
                    away_team_data = api_match.get('away_team', {})
                    
                    home_team = home_team_data.get('name', '')
                    away_team = away_team_data.get('name', '')
                    home_score = home_team_data.get('goals')
                    away_score = away_team_data.get('goals')
                    
                    if not all([home_team, away_team, home_score is not None, away_score is not None]):
                        continue
                    
                    # Find matching match in database
                    # Try exact match first, then fuzzy match
                    if include_already_finished:
                        match = Match.query.filter(
                            db.or_(
                                db.and_(
                                    Match.team_home == home_team,
                                    Match.team_away == away_team
                                ),
                                db.and_(
                                    Match.team_home.ilike(f'%{home_team}%'),
                                    Match.team_away.ilike(f'%{away_team}%')
                                )
                            )
                        ).first()
                    else:
                        match = Match.query.filter(
                            db.and_(
                                db.or_(
                                    db.and_(
                                        Match.team_home == home_team,
                                        Match.team_away == away_team
                                    ),
                                    db.and_(
                                        Match.team_home.ilike(f'%{home_team}%'),
                                        Match.team_away.ilike(f'%{away_team}%')
                                    )
                                ),
                                Match.is_finished == False
                            )
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
    
    def sync_matches_from_api(self):
        """
        Sync all matches from API to database
        Creates new matches if they don't exist
        
        Returns:
            Tuple of (created_count, updated_count)
        """
        if not self.app:
            print("⚠️  App context not available")
            return (0, 0)
        
        with self.app.app_context():
            try:
                api_matches = self.fetch_world_cup_matches()
                
                if not api_matches:
                    print("ℹ️  No matches found from API")
                    return (0, 0)
                
                created_count = 0
                updated_count = 0
                
                for api_match in api_matches:
                    # FILTER: Only process 2026 matches, skip 2022 data
                    match_date_str = api_match.get('datetime', '')
                    if match_date_str and '2022' in match_date_str:
                        continue  # Skip 2022 World Cup matches
                    
                    home_team_data = api_match.get('home_team', {})
                    away_team_data = api_match.get('away_team', {})
                    
                    home_team = home_team_data.get('name', '')
                    away_team = away_team_data.get('name', '')
                    
                    if not home_team or not away_team:
                        continue
                    
                    # Parse match date
                    match_date_str = api_match.get('datetime', '')
                    try:
                        match_date = datetime.fromisoformat(match_date_str.replace('Z', '+00:00'))
                    except:
                        continue
                    
                    # Get stage name
                    stage = api_match.get('stage_name', 'Group Stage')
                    
                    # Check if match exists
                    match = Match.query.filter(
                        db.or_(
                            db.and_(
                                Match.team_home == home_team,
                                Match.team_away == away_team
                            ),
                            db.and_(
                                Match.team_home.ilike(f'%{home_team}%'),
                                Match.team_away.ilike(f'%{away_team}%')
                            )
                        )
                    ).first()
                    
                    if match:
                        # Update existing match if status changed
                        status = api_match.get('status', '')
                        if status == 'completed' and not match.is_finished:
                            match.home_score = home_team_data.get('goals')
                            match.away_score = away_team_data.get('goals')
                            match.is_finished = True
                            
                            # Calculate points for predictions
                            for prediction in match.predictions:
                                prediction.points_earned = prediction.calculate_points()
                            
                            updated_count += 1
                            print(f"✅ Updated: {home_team} vs {away_team}")
                    else:
                        # Create new match
                        new_match = Match(
                            team_home=home_team,
                            team_away=away_team,
                            match_date=match_date,
                            stage=stage
                        )
                        
                        # If match is completed, add scores
                        if api_match.get('status') == 'completed':
                            new_match.home_score = home_team_data.get('goals')
                            new_match.away_score = away_team_data.get('goals')
                            new_match.is_finished = True
                        
                        db.session.add(new_match)
                        created_count += 1
                        print(f"✅ Created: {home_team} vs {away_team}")
                
                db.session.commit()
                
                if created_count > 0 or updated_count > 0:
                    print(f"✅ Sync complete: {created_count} created, {updated_count} updated")
                else:
                    print("ℹ️  No changes needed")
                
                return (created_count, updated_count)
                
            except Exception as e:
                print(f"❌ Error syncing matches: {e}")
                db.session.rollback()
                return (0, 0)
    
    def get_live_scores(self):
        """
        Get current live scores from API
        Returns matches that are currently in progress
        
        Returns:
            List of live match data
        """
        try:
            api_matches = self.fetch_world_cup_matches()
            
            live_matches = []
            for match in api_matches:
                status = match.get('status', '')
                # Check for in-progress statuses
                if status in ['in_progress', 'live', 'first_half', 'second_half', 'halftime']:
                    live_matches.append({
                        'home_team': match.get('home_team', {}).get('name', ''),
                        'away_team': match.get('away_team', {}).get('name', ''),
                        'home_score': match.get('home_team', {}).get('goals', 0),
                        'away_score': match.get('away_team', {}).get('goals', 0),
                        'status': status,
                        'venue': match.get('venue', ''),
                        'datetime': match.get('datetime', '')
                    })
            
            return live_matches
            
        except Exception as e:
            print(f"❌ Error fetching live scores: {e}")
            return []
    
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
