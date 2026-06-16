#!/usr/bin/env python3
"""
Match Sync Utility Script
Syncs all matches from worldcupjson.net API to your database
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app
from backend.match_updater import MatchUpdater

def main():
    """Main sync function"""
    print("=" * 60)
    print("World Cup Match Sync Utility")
    print("=" * 60)
    print()
    
    updater = MatchUpdater(app)
    
    # Test API connection first
    print("1. Testing API connection...")
    matches = updater.fetch_world_cup_matches()
    if not matches:
        print("❌ Failed to connect to API")
        return
    print(f"✅ Connected! Found {len(matches)} matches from API")
    print()
    
    # Fetch teams
    print("2. Fetching teams...")
    teams_data = updater.fetch_teams()
    if teams_data:
        groups = teams_data.get('groups', [])
        total_teams = sum(len(group.get('teams', [])) for group in groups)
        print(f"✅ Found {total_teams} teams in {len(groups)} groups")
    print()
    
    # Sync matches
    print("3. Syncing matches to database...")
    created, updated = updater.sync_matches_from_api()
    print()
    
    # Summary
    print("=" * 60)
    print("SYNC SUMMARY")
    print("=" * 60)
    print(f"Matches created: {created}")
    print(f"Matches updated: {updated}")
    print(f"Total matches in API: {len(matches)}")
    print()
    
    # Show sample matches
    if matches:
        print("Sample matches from API:")
        for i, match in enumerate(matches[:5], 1):
            home = match.get('home_team', {}).get('name', 'Unknown')
            away = match.get('away_team', {}).get('name', 'Unknown')
            status = match.get('status', 'unknown')
            print(f"  {i}. {home} vs {away} - Status: {status}")
    
    print()
    print("✅ Sync complete!")
    print()
    print("Next steps:")
    print("  - Start your Flask app: python -m backend.app")
    print("  - Visit admin panel to manage matches")
    print("  - Automatic updates run every 15 minutes")

if __name__ == '__main__':
    main()

# Made with Bob
