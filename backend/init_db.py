#!/usr/bin/env python3
"""
Initialize the database with proper schema
"""
import os
import sys

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import app, db
from backend.models import User, Match, Prediction

def init_database():
    """Initialize database with all tables"""
    with app.app_context():
        # Drop all tables (if they exist)
        db.drop_all()
        print("Dropped existing tables (if any)")
        
        # Create all tables
        db.create_all()
        print("Created all tables")
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\nTables created: {tables}")
        
        # Verify user table has is_admin column
        if 'user' in tables:
            columns = [col['name'] for col in inspector.get_columns('user')]
            print(f"User table columns: {columns}")
            
            if 'is_admin' in columns:
                print("\n✅ Database initialized successfully with is_admin column!")
            else:
                print("\n❌ ERROR: is_admin column not found in user table!")
                return False
        else:
            print("\n❌ ERROR: user table not created!")
            return False
        
        return True

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)

# Made with Bob
