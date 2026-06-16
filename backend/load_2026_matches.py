#!/usr/bin/env python3
"""
Load 2026 World Cup Matches Script
Clears all existing matches and loads only 2026 World Cup matches from schedule.csv
"""

import sys
import os
import csv
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app
from backend.models import db, Match, Prediction

def parse_date_time(date_str, time_str):
    """
    Parse date and time from CSV format
    
    Args:
        date_str: Date string like "June 11, 2026"
        time_str: Time string like "12:30 a.m. (June 12, 2026)"
    
    Returns:
        datetime object
    """
    try:
        # Extract the actual date from time_str (the date in parentheses)
        if '(' in time_str and ')' in time_str:
            actual_date = time_str.split('(')[1].split(')')[0].strip()
        else:
            actual_date = date_str
        
        # Extract time
        time_part = time_str.split('(')[0].strip()
        
        # Parse the date
        date_obj = datetime.strptime(actual_date, "%B %d, %Y")
        
        # Parse time (handle a.m./p.m.)
        time_part = time_part.replace('.', '').upper()  # Remove dots and uppercase
        
        try:
            time_obj = datetime.strptime(time_part, "%I:%M %p")
        except:
            # If parsing fails, default to noon
            time_obj = datetime.strptime("12:00 PM", "%I:%M %p")
        
        # Combine date and time
        final_datetime = datetime.combine(date_obj.date(), time_obj.time())
        
        return final_datetime
    except Exception as e:
        print(f"⚠️  Error parsing date/time '{date_str}' / '{time_str}': {e}")
        # Return a default date if parsing fails
        return datetime(2026, 6, 11, 12, 0)

def extract_teams(match_str):
    """
    Extract team names from match string
    
    Args:
        match_str: String like "Mexico v/s South Africa" or "Round of 32 - 1"
    
    Returns:
        Tuple of (home_team, away_team) or None if it's a placeholder match
    """
    # Check if it's a knockout stage placeholder
    if 'Round of' in match_str or 'Quarterfinal' in match_str or 'Semifinal' in match_str or 'Final' in match_str or 'Third-place' in match_str:
        return None
    
    # Split by v/s or vs
    if ' v/s ' in match_str:
        teams = match_str.split(' v/s ')
    elif ' vs ' in match_str:
        teams = match_str.split(' vs ')
    elif ' v. ' in match_str:
        teams = match_str.split(' v. ')
    else:
        return None
    
    if len(teams) == 2:
        return (teams[0].strip(), teams[1].strip())
    
    return None

def determine_stage(date_str, match_str):
    """
    Determine the stage of the match
    
    Args:
        date_str: Date string
        match_str: Match description
    
    Returns:
        Stage name
    """
    if 'Round of 32' in match_str:
        return 'Round of 32'
    elif 'Round of 16' in match_str:
        return 'Round of 16'
    elif 'Quarterfinal' in match_str:
        return 'Quarter-finals'
    elif 'Semifinal' in match_str:
        return 'Semi-finals'
    elif 'Third-place' in match_str:
        return 'Third Place'
    elif 'Final' in match_str and 'Quarterfinal' not in match_str and 'Semifinal' not in match_str:
        return 'Final'
    else:
        return 'Group Stage'

def load_2026_matches():
    """Load 2026 World Cup matches from schedule.csv"""
    print("=" * 70)
    print("LOADING 2026 WORLD CUP MATCHES")
    print("=" * 70)
    print()
    
    with app.app_context():
        # Step 1: Clear all existing matches and predictions
        print("🗑️  Step 1: Clearing existing data...")
        
        # Delete all predictions first (due to foreign key constraints)
        prediction_count = Prediction.query.count()
        Prediction.query.delete()
        print(f"   ✅ Deleted {prediction_count} predictions")
        
        # Delete all matches
        match_count = Match.query.count()
        Match.query.delete()
        print(f"   ✅ Deleted {match_count} matches (2022 data removed)")
        
        db.session.commit()
        print()
        
        # Step 2: Load 2026 matches from CSV
        print("📥 Step 2: Loading 2026 matches from schedule.csv...")
        
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schedule.csv')
        
        if not os.path.exists(csv_path):
            print(f"❌ Error: schedule.csv not found at {csv_path}")
            return
        
        matches_added = 0
        matches_skipped = 0
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                date_str = row.get('Date', '').strip()
                match_str = row.get('Match', '').strip()
                time_str = row.get('Kick-Off Time in IST', '').strip()
                venue_str = row.get('Venue', '').strip()
                
                # Extract teams
                teams = extract_teams(match_str)
                
                if not teams:
                    # Skip placeholder matches (knockout rounds TBD)
                    matches_skipped += 1
                    continue
                
                home_team, away_team = teams
                
                # Parse date and time
                match_date = parse_date_time(date_str, time_str)
                
                # Determine stage
                stage = determine_stage(date_str, match_str)
                
                # Create match
                new_match = Match(
                    team_home=home_team,
                    team_away=away_team,
                    match_date=match_date,
                    stage=stage,
                    is_finished=False
                )
                
                db.session.add(new_match)
                matches_added += 1
                
                print(f"   ✅ Added: {home_team} vs {away_team} ({stage}) - {match_date.strftime('%b %d, %Y')}")
        
        # Commit all matches
        db.session.commit()
        
        print()
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"✅ Successfully loaded {matches_added} matches for 2026 World Cup")
        print(f"ℹ️  Skipped {matches_skipped} placeholder matches (knockout rounds TBD)")
        print()
        
        # Show breakdown by stage
        print("Matches by stage:")
        stages = db.session.query(Match.stage, db.func.count(Match.id)).group_by(Match.stage).all()
        for stage, count in stages:
            print(f"   • {stage}: {count} matches")
        
        print()
        print("=" * 70)
        print("✅ DATABASE UPDATED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("  1. Start your Flask app: python -m backend.app")
        print("  2. The app will now show only 2026 World Cup matches")
        print("  3. Users can make predictions for upcoming matches")
        print("  4. Match results will auto-update from the API when available")
        print()

if __name__ == '__main__':
    try:
        load_2026_matches()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Made with Bob