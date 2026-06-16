#!/usr/bin/env python3
"""
Script to remove all URL links from past (finished) matches in the database.
This will set live_stream_url to NULL for all matches where is_finished = True.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from models import db, Match
from flask import Flask

def create_app():
    """Create Flask app with database configuration"""
    app = Flask(__name__)
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/worldcup.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    return app

def remove_past_match_urls():
    """Remove URLs from all finished matches"""
    app = create_app()
    
    with app.app_context():
        # Find all finished matches with URLs
        finished_matches = Match.query.filter(
            Match.is_finished == True,
            Match.live_stream_url.isnot(None)
        ).all()
        
        if not finished_matches:
            print("No finished matches with URLs found.")
            return
        
        print(f"Found {len(finished_matches)} finished matches with URLs:")
        print("-" * 80)
        
        for match in finished_matches:
            print(f"Match ID {match.id}: {match.team_home} vs {match.team_away}")
            print(f"  Date: {match.match_date}")
            print(f"  Score: {match.home_score} - {match.away_score}")
            print(f"  Current URL: {match.live_stream_url}")
            print()
        
        # Ask for confirmation
        response = input(f"\nDo you want to remove URLs from these {len(finished_matches)} matches? (yes/no): ")
        
        if response.lower() not in ['yes', 'y']:
            print("Operation cancelled.")
            return
        
        # Remove URLs
        count = 0
        for match in finished_matches:
            match.live_stream_url = None
            count += 1
        
        # Commit changes
        db.session.commit()
        
        print(f"\n✓ Successfully removed URLs from {count} finished matches!")
        print("\nVerifying changes...")
        
        # Verify
        remaining = Match.query.filter(
            Match.is_finished == True,
            Match.live_stream_url.isnot(None)
        ).count()
        
        if remaining == 0:
            print("✓ Verification successful: No URLs remain in finished matches.")
        else:
            print(f"⚠ Warning: {remaining} finished matches still have URLs.")

if __name__ == '__main__':
    print("=" * 80)
    print("Remove URLs from Past Matches")
    print("=" * 80)
    print()
    
    try:
        remove_past_match_urls()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Made with Bob
