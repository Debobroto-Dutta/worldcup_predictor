#!/usr/bin/env python3
"""
Script to remove all URL links from past (finished) matches in the database.
This script will:
1. Check if live_stream_url column exists, add it if not
2. Remove URLs from all finished matches
"""

import sqlite3
import os

def remove_past_match_urls():
    """Remove URLs from all finished matches"""
    
    # Database path
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'worldcup.db')
    
    if not os.path.exists(db_path):
        print(f"✗ Error: Database not found at {db_path}")
        return
    
    print(f"Connecting to database: {db_path}")
    print()
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if live_stream_url column exists
        cursor.execute("PRAGMA table_info(match)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'live_stream_url' not in columns:
            print("⚠ live_stream_url column does not exist in the database.")
            print("This means no URLs have been stored yet.")
            print("\nNo action needed - the database is already clean!")
            return
        
        print("✓ live_stream_url column exists")
        print()
        
        # Find all finished matches with URLs
        cursor.execute("""
            SELECT id, team_home, team_away, match_date, home_score, away_score, live_stream_url
            FROM match
            WHERE is_finished = 1 AND live_stream_url IS NOT NULL AND live_stream_url != ''
        """)
        
        finished_matches = cursor.fetchall()
        
        if not finished_matches:
            print("✓ No finished matches with URLs found.")
            print("The database is already clean!")
            return
        
        print(f"Found {len(finished_matches)} finished matches with URLs:")
        print("-" * 80)
        
        for match in finished_matches:
            match_id, home, away, date, home_score, away_score, url = match
            print(f"Match ID {match_id}: {home} vs {away}")
            print(f"  Date: {date}")
            print(f"  Score: {home_score} - {away_score}")
            print(f"  Current URL: {url}")
            print()
        
        # Ask for confirmation
        response = input(f"\nDo you want to remove URLs from these {len(finished_matches)} matches? (yes/no): ")
        
        if response.lower() not in ['yes', 'y']:
            print("Operation cancelled.")
            return
        
        # Remove URLs
        cursor.execute("""
            UPDATE match
            SET live_stream_url = NULL
            WHERE is_finished = 1 AND live_stream_url IS NOT NULL
        """)
        
        count = cursor.rowcount
        conn.commit()
        
        print(f"\n✓ Successfully removed URLs from {count} finished matches!")
        print("\nVerifying changes...")
        
        # Verify
        cursor.execute("""
            SELECT COUNT(*)
            FROM match
            WHERE is_finished = 1 AND live_stream_url IS NOT NULL AND live_stream_url != ''
        """)
        
        remaining = cursor.fetchone()[0]
        
        if remaining == 0:
            print("✓ Verification successful: No URLs remain in finished matches.")
        else:
            print(f"⚠ Warning: {remaining} finished matches still have URLs.")
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

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
        exit(1)

# Made with Bob
