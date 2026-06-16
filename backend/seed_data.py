"""
Script to seed the database with FIFA World Cup 2026 matches
Run this after initializing the database
"""

from backend.app import app, db
from backend.models import Match
from datetime import datetime

def seed_matches():
    """Add FIFA World Cup 2026 matches from official schedule"""
    
    # Clear existing matches
    Match.query.delete()
    print("Cleared existing matches")
    
    matches = [
        # Group Stage Matches
        {'team_home': 'Mexico', 'team_away': 'South Africa', 'match_date': datetime(2026, 6, 12, 0, 30), 'stage': 'Group Stage'},
        {'team_home': 'South Korea', 'team_away': 'Czechia', 'match_date': datetime(2026, 6, 12, 7, 30), 'stage': 'Group Stage'},
        {'team_home': 'Canada', 'team_away': 'Bosnia and Herzegovina', 'match_date': datetime(2026, 6, 13, 0, 30), 'stage': 'Group Stage'},
        {'team_home': 'USA', 'team_away': 'Paraguay', 'match_date': datetime(2026, 6, 14, 6, 30), 'stage': 'Group Stage'},
        {'team_home': 'Qatar', 'team_away': 'Switzerland', 'match_date': datetime(2026, 6, 14, 0, 30), 'stage': 'Group Stage'},
        {'team_home': 'Brazil', 'team_away': 'Morocco', 'match_date': datetime(2026, 6, 14, 3, 30), 'stage': 'Group Stage'},
        {'team_home': 'Haiti', 'team_away': 'Scotland', 'match_date': datetime(2026, 6, 14, 6, 30), 'stage': 'Group Stage'},
        {'team_home': 'Australia', 'team_away': 'Turkey', 'match_date': datetime(2026, 6, 14, 9, 30), 'stage': 'Group Stage'},
        {'team_home': 'Germany', 'team_away': 'Curacao', 'match_date': datetime(2026, 6, 14, 22, 30), 'stage': 'Group Stage'},
        {'team_home': 'Netherlands', 'team_away': 'Japan', 'match_date': datetime(2026, 6, 15, 1, 30), 'stage': 'Group Stage'},
        {'team_home': 'Ivory Coast', 'team_away': 'Ecuador', 'match_date': datetime(2026, 6, 15, 4, 30), 'stage': 'Group Stage'},
        {'team_home': 'Sweden', 'team_away': 'Tunisia', 'match_date': datetime(2026, 6, 15, 7, 30), 'stage': 'Group Stage'},
        {'team_home': 'Spain', 'team_away': 'Cape Verde', 'match_date': datetime(2026, 6, 15, 21, 30), 'stage': 'Group Stage'},
        {'team_home': 'Belgium', 'team_away': 'Egypt', 'match_date': datetime(2026, 6, 16, 0, 30), 'stage': 'Group Stage'},
        {'team_home': 'Saudi Arabia', 'team_away': 'Uruguay', 'match_date': datetime(2026, 6, 16, 3, 30), 'stage': 'Group Stage'},
        {'team_home': 'Iran', 'team_away': 'New Zealand', 'match_date': datetime(2026, 6, 16, 6, 30), 'stage': 'Group Stage'},
        {'team_home': 'France', 'team_away': 'Senegal', 'match_date': datetime(2026, 6, 17, 0, 30), 'stage': 'Group Stage'},
        {'team_home': 'Iraq', 'team_away': 'Norway', 'match_date': datetime(2026, 6, 17, 3, 30), 'stage': 'Group Stage'},
        {'team_home': 'Argentina', 'team_away': 'Algeria', 'match_date': datetime(2026, 6, 17, 6, 30), 'stage': 'Group Stage'},
        {'team_home': 'Austria', 'team_away': 'Jordan', 'match_date': datetime(2026, 6, 17, 9, 30), 'stage': 'Group Stage'},
        {'team_home': 'Portugal', 'team_away': 'DR Congo', 'match_date': datetime(2026, 6, 17, 22, 30), 'stage': 'Group Stage'},
        {'team_home': 'England', 'team_away': 'Croatia', 'match_date': datetime(2026, 6, 18, 1, 30), 'stage': 'Group Stage'},
        {'team_home': 'Ghana', 'team_away': 'Panama', 'match_date': datetime(2026, 6, 18, 4, 30), 'stage': 'Group Stage'},
        {'team_home': 'Uzbekistan', 'team_away': 'Colombia', 'match_date': datetime(2026, 6, 18, 7, 30), 'stage': 'Group Stage'},
        {'team_home': 'Czechia', 'team_away': 'South Africa', 'match_date': datetime(2026, 6, 18, 21, 30), 'stage': 'Group Stage'},
        {'team_home': 'Switzerland', 'team_away': 'Bosnia and Herzegovina', 'match_date': datetime(2026, 6, 19, 0, 30), 'stage': 'Group Stage'},
        {'team_home': 'Canada', 'team_away': 'Qatar', 'match_date': datetime(2026, 6, 19, 3, 30), 'stage': 'Group Stage'},
        {'team_home': 'Mexico', 'team_away': 'South Korea', 'match_date': datetime(2026, 6, 19, 6, 30), 'stage': 'Group Stage'},
        {'team_home': 'USA', 'team_away': 'Australia', 'match_date': datetime(2026, 6, 20, 0, 30), 'stage': 'Group Stage'},
        {'team_home': 'Scotland', 'team_away': 'Morocco', 'match_date': datetime(2026, 6, 20, 3, 30), 'stage': 'Group Stage'},
        {'team_home': 'Brazil', 'team_away': 'Haiti', 'match_date': datetime(2026, 6, 20, 6, 30), 'stage': 'Group Stage'},
        {'team_home': 'Turkey', 'team_away': 'Paraguay', 'match_date': datetime(2026, 6, 20, 9, 30), 'stage': 'Group Stage'},
        {'team_home': 'Netherlands', 'team_away': 'Sweden', 'match_date': datetime(2026, 6, 20, 22, 30), 'stage': 'Group Stage'},
        {'team_home': 'Germany', 'team_away': 'Ivory Coast', 'match_date': datetime(2026, 6, 21, 1, 30), 'stage': 'Group Stage'},
        {'team_home': 'Ecuador', 'team_away': 'Curacao', 'match_date': datetime(2026, 6, 21, 5, 30), 'stage': 'Group Stage'},
        {'team_home': 'Tunisia', 'team_away': 'Japan', 'match_date': datetime(2026, 6, 21, 9, 30), 'stage': 'Group Stage'},
        {'team_home': 'Spain', 'team_away': 'Saudi Arabia', 'match_date': datetime(2026, 6, 21, 21, 30), 'stage': 'Group Stage'},
        {'team_home': 'Belgium', 'team_away': 'Iran', 'match_date': datetime(2026, 6, 22, 0, 30), 'stage': 'Group Stage'},
        {'team_home': 'Uruguay', 'team_away': 'Cape Verde', 'match_date': datetime(2026, 6, 22, 3, 30), 'stage': 'Group Stage'},
        {'team_home': 'New Zealand', 'team_away': 'Egypt', 'match_date': datetime(2026, 6, 22, 6, 30), 'stage': 'Group Stage'},
        {'team_home': 'Argentina', 'team_away': 'Austria', 'match_date': datetime(2026, 6, 22, 22, 30), 'stage': 'Group Stage'},
        {'team_home': 'France', 'team_away': 'Iraq', 'match_date': datetime(2026, 6, 23, 2, 30), 'stage': 'Group Stage'},
        {'team_home': 'Norway', 'team_away': 'Senegal', 'match_date': datetime(2026, 6, 23, 5, 30), 'stage': 'Group Stage'},
        {'team_home': 'Jordan', 'team_away': 'Algeria', 'match_date': datetime(2026, 6, 23, 8, 30), 'stage': 'Group Stage'},
        {'team_home': 'Portugal', 'team_away': 'Uzbekistan', 'match_date': datetime(2026, 6, 23, 22, 30), 'stage': 'Group Stage'},
        {'team_home': 'England', 'team_away': 'Ghana', 'match_date': datetime(2026, 6, 24, 1, 30), 'stage': 'Group Stage'},
        {'team_home': 'Panama', 'team_away': 'Croatia', 'match_date': datetime(2026, 6, 24, 4, 30), 'stage': 'Group Stage'},
        {'team_home': 'Colombia', 'team_away': 'DR Congo', 'match_date': datetime(2026, 6, 24, 7, 30), 'stage': 'Group Stage'},
        {'team_home': 'Switzerland', 'team_away': 'Canada', 'match_date': datetime(2026, 6, 25, 0, 30), 'stage': 'Group Stage'},
        {'team_home': 'Bosnia and Herzegovina', 'team_away': 'Qatar', 'match_date': datetime(2026, 6, 25, 0, 30), 'stage': 'Group Stage'},
        {'team_home': 'Morocco', 'team_away': 'Haiti', 'match_date': datetime(2026, 6, 25, 3, 30), 'stage': 'Group Stage'},
        {'team_home': 'Scotland', 'team_away': 'Brazil', 'match_date': datetime(2026, 6, 25, 3, 30), 'stage': 'Group Stage'},
        {'team_home': 'South Africa', 'team_away': 'South Korea', 'match_date': datetime(2026, 6, 25, 6, 30), 'stage': 'Group Stage'},
        {'team_home': 'Czechia', 'team_away': 'Mexico', 'match_date': datetime(2026, 6, 25, 6, 30), 'stage': 'Group Stage'},
        {'team_home': 'Curacao', 'team_away': 'Ivory Coast', 'match_date': datetime(2026, 6, 26, 1, 30), 'stage': 'Group Stage'},
        {'team_home': 'Ecuador', 'team_away': 'Germany', 'match_date': datetime(2026, 6, 26, 1, 30), 'stage': 'Group Stage'},
        {'team_home': 'Tunisia', 'team_away': 'Netherlands', 'match_date': datetime(2026, 6, 26, 4, 30), 'stage': 'Group Stage'},
        {'team_home': 'Japan', 'team_away': 'Sweden', 'match_date': datetime(2026, 6, 26, 4, 30), 'stage': 'Group Stage'},
        {'team_home': 'Turkey', 'team_away': 'USA', 'match_date': datetime(2026, 6, 26, 7, 30), 'stage': 'Group Stage'},
        {'team_home': 'Paraguay', 'team_away': 'Australia', 'match_date': datetime(2026, 6, 26, 7, 30), 'stage': 'Group Stage'},
        {'team_home': 'Norway', 'team_away': 'France', 'match_date': datetime(2026, 6, 27, 0, 30), 'stage': 'Group Stage'},
        {'team_home': 'Senegal', 'team_away': 'Iraq', 'match_date': datetime(2026, 6, 27, 0, 30), 'stage': 'Group Stage'},
        {'team_home': 'Cape Verde', 'team_away': 'Saudi Arabia', 'match_date': datetime(2026, 6, 27, 5, 30), 'stage': 'Group Stage'},
        {'team_home': 'Uruguay', 'team_away': 'Spain', 'match_date': datetime(2026, 6, 27, 5, 30), 'stage': 'Group Stage'},
        {'team_home': 'New Zealand', 'team_away': 'Belgium', 'match_date': datetime(2026, 6, 27, 8, 30), 'stage': 'Group Stage'},
        {'team_home': 'Egypt', 'team_away': 'Iran', 'match_date': datetime(2026, 6, 27, 8, 30), 'stage': 'Group Stage'},
        {'team_home': 'Panama', 'team_away': 'England', 'match_date': datetime(2026, 6, 28, 2, 30), 'stage': 'Group Stage'},
        {'team_home': 'Croatia', 'team_away': 'Ghana', 'match_date': datetime(2026, 6, 28, 2, 30), 'stage': 'Group Stage'},
        {'team_home': 'Colombia', 'team_away': 'Portugal', 'match_date': datetime(2026, 6, 28, 5, 0), 'stage': 'Group Stage'},
        {'team_home': 'DR Congo', 'team_away': 'Uzbekistan', 'match_date': datetime(2026, 6, 28, 5, 0), 'stage': 'Group Stage'},
        {'team_home': 'Algeria', 'team_away': 'Austria', 'match_date': datetime(2026, 6, 28, 7, 30), 'stage': 'Group Stage'},
        {'team_home': 'Jordan', 'team_away': 'Argentina', 'match_date': datetime(2026, 6, 28, 7, 30), 'stage': 'Group Stage'},
        
        # Round of 32
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 6, 29, 0, 30), 'stage': 'Round of 32'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 6, 29, 22, 30), 'stage': 'Round of 32'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 6, 30, 2, 0), 'stage': 'Round of 32'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 6, 30, 6, 30), 'stage': 'Round of 32'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 6, 30, 22, 30), 'stage': 'Round of 32'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 1, 2, 30), 'stage': 'Round of 32'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 1, 6, 30), 'stage': 'Round of 32'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 1, 21, 30), 'stage': 'Round of 32'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 2, 1, 30), 'stage': 'Round of 32'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 2, 5, 30), 'stage': 'Round of 32'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 3, 0, 30), 'stage': 'Round of 32'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 3, 4, 30), 'stage': 'Round of 32'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 3, 8, 30), 'stage': 'Round of 32'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 3, 23, 30), 'stage': 'Round of 32'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 4, 3, 30), 'stage': 'Round of 32'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 4, 7, 0), 'stage': 'Round of 32'},
        
        # Round of 16
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 4, 10, 30), 'stage': 'Round of 16'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 5, 2, 30), 'stage': 'Round of 16'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 6, 1, 30), 'stage': 'Round of 16'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 6, 5, 30), 'stage': 'Round of 16'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 7, 0, 30), 'stage': 'Round of 16'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 7, 5, 30), 'stage': 'Round of 16'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 7, 21, 30), 'stage': 'Round of 16'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 8, 1, 30), 'stage': 'Round of 16'},
        
        # Quarter Finals
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 10, 1, 30), 'stage': 'Quarter Final'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 11, 0, 30), 'stage': 'Quarter Final'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 12, 2, 30), 'stage': 'Quarter Final'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 12, 6, 30), 'stage': 'Quarter Final'},
        
        # Semi Finals
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 15, 0, 30), 'stage': 'Semi Final'},
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 16, 0, 30), 'stage': 'Semi Final'},
        
        # Third Place
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 19, 2, 30), 'stage': 'Third Place'},
        
        # Final
        {'team_home': 'TBD', 'team_away': 'TBD', 'match_date': datetime(2026, 7, 20, 0, 30), 'stage': 'Final'},
    ]
    
    for match_data in matches:
        match = Match(**match_data)
        db.session.add(match)
    
    db.session.commit()
    print(f"Successfully added {len(matches)} matches to the database!")

if __name__ == '__main__':
    with app.app_context():
        seed_matches()

# Made with Bob
