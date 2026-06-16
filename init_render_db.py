#!/usr/bin/env python3
"""
Initialize database on Render
Run this once after deployment: python init_render_db.py
"""
import sys
import os

# Ensure we're in the right directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import app, db
from backend.models import User

def init_database():
    """Initialize database and create admin user"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created")
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("\nCreating default admin user...")
            admin = User(username='admin', email='admin@worldcup.com')
            admin.set_password('admin123')  # Change this password!
            admin.is_admin = True
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created")
            print("  Username: admin")
            print("  Password: admin123")
            print("  ⚠️  IMPORTANT: Change this password immediately!")
        else:
            print("\n✓ Admin user already exists")
        
        print("\n✅ Database initialization complete!")
        print("\nNext steps:")
        print("1. Login with admin credentials")
        print("2. Change admin password in the admin panel")
        print("3. Add match data using the admin panel")

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

# Made with Bob
