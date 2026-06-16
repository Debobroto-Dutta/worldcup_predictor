"""
Database migration script to add live streaming URL and ESPN match ID fields
Run this once to update your existing database
"""
from flask import Flask
from backend.models import db
import os

app = Flask(__name__)

# Database configuration
database_url = os.environ.get('DATABASE_URL', 'sqlite:///worldcup.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def add_live_fields():
    """Add live_stream_url and espn_match_id columns to Match table"""
    with app.app_context():
        try:
            # Check if we're using SQLite or PostgreSQL
            if 'sqlite' in database_url:
                # SQLite
                db.engine.execute('ALTER TABLE match ADD COLUMN live_stream_url VARCHAR(500)')
                db.engine.execute('ALTER TABLE match ADD COLUMN espn_match_id VARCHAR(100)')
                print("✅ Successfully added live_stream_url and espn_match_id columns (SQLite)")
            else:
                # PostgreSQL
                db.engine.execute('ALTER TABLE match ADD COLUMN IF NOT EXISTS live_stream_url VARCHAR(500)')
                db.engine.execute('ALTER TABLE match ADD COLUMN IF NOT EXISTS espn_match_id VARCHAR(100)')
                print("✅ Successfully added live_stream_url and espn_match_id columns (PostgreSQL)")
            
            print("✅ Database migration completed successfully!")
            print("\nYou can now:")
            print("1. Set live streaming URLs for matches")
            print("2. Use ESPN API integration for live scores")
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            print("\nNote: If columns already exist, this is normal and can be ignored.")

if __name__ == '__main__':
    print("🔄 Starting database migration...")
    print(f"Database: {database_url}")
    add_live_fields()

# Made with Bob