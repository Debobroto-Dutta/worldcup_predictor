"""
Database migration script to add is_admin column to existing database
Run this if you already have a database and need to add the admin feature
"""

from app import app, db
from models import User
import sqlite3

def migrate_database():
    """Add is_admin column to user table"""
    
    # Get database path from app config
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    
    print(f"Migrating database: {db_path}")
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if is_admin column exists
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'is_admin' in columns:
            print("✓ is_admin column already exists")
        else:
            print("Adding is_admin column...")
            cursor.execute("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0")
            conn.commit()
            print("✓ is_admin column added successfully")
        
        conn.close()
        print("\n✅ Database migration completed successfully!")
        print("\nYou can now create admin users.")
        
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        print("\nIf you continue to have issues, you may need to:")
        print("1. Backup your database")
        print("2. Delete the database file")
        print("3. Run the application to create a fresh database")

if __name__ == '__main__':
    with app.app_context():
        migrate_database()

# Made with Bob
