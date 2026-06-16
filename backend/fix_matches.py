#!/usr/bin/env python3
"""
Fix Matches Script
Updates all past matches with scores from the API
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app
from backend.match_updater import MatchUpdater
from backend.models import db, Match

def fix_all_matches():
    """Update all matches with data from API"""
    print("=" * 60)
    print("Fixing All Matches - Updating Scores from API")
    print("=" * 60)
    print()
    
    updater = MatchUpdater(app)
    
    with app.app_context():
        # Get current matches in database
        db_matches = Match.query.all()
        print(f"📊 Found {len(db_matches)} matches in database")
        print()
        
        # Fetch all matches from API
        print("🔄 Fetching matches from API...")
        api_matches = updater.fetch_world_cup_matches()
        
        if not api_matches:
            print("❌ Failed to fetch matches from API")
            return
        
        print(f"✅ Found {len(api_matches)} matches from API")
        print()
        
        # Update each match
        updated_count = 0
        created_count = 0
        
        for api_match in api_matches:
            home_team_data = api_match.get('home_team', {})
            away_team_data = api_match.get('away_team', {})
            
            home_team = home_team_data.get('name', '')
            away_team = away_team_data.get('name', '')
            status = api_match.get('status', '')
            
            if not home_team or not away_team:
                continue
            
            # Find match in database
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
                # Update existing match
                if status == 'completed':
                    home_score = home_team_data.get('goals')
                    away_score = away_team_data.get('goals')
                    
                    if home_score is not None and away_score is not None:
                        match.home_score = home_score
                        match.away_score = away_score
                        match.is_finished = True
                        
                        # Calculate points for predictions
                        for prediction in match.predictions:
                            prediction.points_earned = prediction.calculate_points()
                        
                        updated_count += 1
                        print(f"✅ Updated: {home_team} {home_score}-{away_score} {away_team}")
                    else:
                        print(f"⚠️  Skipped: {home_team} vs {away_team} (no scores)")
                else:
                    print(f"ℹ️  Skipped: {home_team} vs {away_team} (status: {status})")
            else:
                # Create new match if it doesn't exist
                from datetime import datetime
                
                match_date_str = api_match.get('datetime', '')
                try:
                    match_date = datetime.fromisoformat(match_date_str.replace('Z', '+00:00'))
                except:
                    continue
                
                stage = api_match.get('stage_name', 'Group Stage')
                
                new_match = Match(
                    team_home=home_team,
                    team_away=away_team,
                    match_date=match_date,
                    stage=stage
                )
                
                if status == 'completed':
                    new_match.home_score = home_team_data.get('goals')
                    new_match.away_score = away_team_data.get('goals')
                    new_match.is_finished = True
                
                db.session.add(new_match)
                created_count += 1
                print(f"✅ Created: {home_team} vs {away_team}")
        
        # Commit all changes
        db.session.commit()
        
        print()
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Matches updated: {updated_count}")
        print(f"Matches created: {created_count}")
        print(f"Total in database: {Match.query.count()}")
        print()
        print("✅ All matches fixed!")
        print()
        
        # Show some finished matches
        finished = Match.query.filter_by(is_finished=True).limit(5).all()
        if finished:
            print("Sample finished matches:")
            for m in finished:
                print(f"  {m.team_home} {m.home_score}-{m.away_score} {m.team_away}")

if __name__ == '__main__':
    fix_all_matches()

# Made with Bob
