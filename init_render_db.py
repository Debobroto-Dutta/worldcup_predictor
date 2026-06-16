#!/usr/bin/env python3
"""
Initialize database for Render deployment
This script runs during the build process to set up the database
"""
import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import app, db
from backend.models import User

def init_render_database():
    """Initialize database for Render"""
    print("🔧 Initializing database for Render...")
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Create default admin user if it doesn't exist
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(username='admin', email='admin@worldcup.com')
                admin.set_password('admin123')
                admin.is_admin = True
                db.session.add(admin)
                db.session.commit()
                print("✅ Default admin user created")
                print("   Username: admin")
                print("   Password: admin123")
                print("   ⚠️  IMPORTANT: Change the admin password after first login!")
            else:
                print("ℹ️  Admin user already exists")
            
            print("✅ Database initialization complete!")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = init_render_database()
    sys.exit(0 if success else 1)

# Made with Bob
