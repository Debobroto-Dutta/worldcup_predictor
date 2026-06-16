#!/usr/bin/env python3
"""
Remove URLs from Past Matches - Production (Render PostgreSQL)

This script removes all URL links from finished matches in your Render PostgreSQL database.
It reads DATABASE_URL from environment variables (Render sets this automatically).

Usage:
1. On Render Shell: python remove_urls_production.py
2. Locally with credentials: export DATABASE_URL='your_postgres_url' && python remove_urls_production.py
"""

import os
import sys

def remove_past_match_urls():
    """Remove URLs from all finished matches in PostgreSQL database"""
    
    # Get DATABASE_URL from environment (Render sets this automatically)
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL environment variable not found!")
        print("\nOptions:")
        print("1. Run this on Render Shell (DATABASE_URL is set automatically)")
        print("2. Set it locally: export DATABASE_URL='postgresql://user:password@host:port/database'")
        print("\nTo get your DATABASE_URL from Render:")
        print("   Dashboard → Your Service → Environment → DATABASE_URL")
        return False
    
    # Fix Render's postgres:// to postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
        print("✓ Fixed DATABASE_URL format (postgres:// → postgresql://)")
    
    print("\n" + "="*80)
    print("  REMOVE URLs FROM PAST MATCHES - PRODUCTION DATABASE")
    print("="*80)
    print(f"\nConnecting to: {database_url.split('@')[1] if '@' in database_url else 'database'}")
    print()
    
    try:
        import psycopg2
    except ImportError:
        print("❌ ERROR: psycopg2 not installed!")
        print("\nInstall it with:")
        print("  pip install psycopg2-binary")
        return False
    
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("✓ Connected to database successfully")
        print()
        
        # Check if live_stream_url column exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='match' AND column_name='live_stream_url'
        """)
        
        if not cursor.fetchone():
            print("⚠ live_stream_url column does not exist in the database.")
            print("This means no URLs have been stored yet.")
            print("\n✓ No action needed - the database is already clean!")
            return True
        
        print("✓ live_stream_url column exists")
        print()
        
        # Find all finished matches with URLs
        cursor.execute("""
            SELECT id, team_home, team_away, match_date, home_score, away_score, live_stream_url
            FROM match
            WHERE is_finished = TRUE AND live_stream_url IS NOT NULL AND live_stream_url != ''
            ORDER BY match_date
        """)
        
        finished_matches = cursor.fetchall()
        
        if not finished_matches:
            print("✓ No finished matches with URLs found.")
            print("The database is already clean!")
            return True
        
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
        print("-" * 80)
        response = input(f"\n⚠️  Do you want to remove URLs from these {len(finished_matches)} matches? (yes/no): ")
        
        if response.lower() not in ['yes', 'y']:
            print("\n❌ Operation cancelled.")
            return False
        
        print("\n🔄 Removing URLs...")
        
        # Remove URLs from finished matches
        cursor.execute("""
            UPDATE match
            SET live_stream_url = NULL
            WHERE is_finished = TRUE AND live_stream_url IS NOT NULL
        """)
        
        count = cursor.rowcount
        conn.commit()
        
        print(f"\n✅ Successfully removed URLs from {count} finished matches!")
        print("\n🔍 Verifying changes...")
        
        # Verify
        cursor.execute("""
            SELECT COUNT(*)
            FROM match
            WHERE is_finished = TRUE AND live_stream_url IS NOT NULL AND live_stream_url != ''
        """)
        
        remaining = cursor.fetchone()[0]
        
        if remaining == 0:
            print("✅ Verification successful: No URLs remain in finished matches.")
            print("\n" + "="*80)
            print("  CLEANUP COMPLETED SUCCESSFULLY!")
            print("="*80)
            return True
        else:
            print(f"⚠️  Warning: {remaining} finished matches still have URLs.")
            return False
            
    except psycopg2.Error as e:
        print(f"\n❌ Database Error: {e}")
        print("\nTroubleshooting:")
        print("1. Verify DATABASE_URL is correct")
        print("2. Check database permissions")
        print("3. Ensure database is accessible")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'conn' in locals():
            conn.close()
            print("\n✓ Database connection closed")

if __name__ == '__main__':
    print("\n" + "="*80)
    print("  World Cup Predictor - Remove URLs from Past Matches")
    print("  Production Database (Render PostgreSQL)")
    print("="*80)
    
    success = remove_past_match_urls()
    
    if success:
        print("\n✅ Task completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Task failed or was cancelled.")
        sys.exit(1)

# Made with Bob
