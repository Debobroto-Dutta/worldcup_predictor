#!/usr/bin/env python3
"""
Generate password hash for admin user
Run: python3 generate_admin_hash.py
"""
import sys
import os

# Add the project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from werkzeug.security import generate_password_hash
    
    # Generate hash for default password
    password = 'admin123'
    hash_value = generate_password_hash(password)
    
    print("\n" + "="*60)
    print("ADMIN PASSWORD HASH GENERATED")
    print("="*60)
    print(f"\nPassword: {password}")
    print(f"\nHash:\n{hash_value}")
    print("\n" + "="*60)
    print("\nCopy the hash above and use it in your SQL INSERT statement:")
    print("\nINSERT INTO \"user\" (username, email, password_hash, is_admin)")
    print("VALUES (")
    print("    'admin',")
    print("    'admin@worldcup.com',")
    print(f"    '{hash_value}',")
    print("    TRUE")
    print(");")
    print("\n" + "="*60)
    
except ImportError:
    print("\n" + "="*60)
    print("ERROR: werkzeug module not found")
    print("="*60)
    print("\nInstalling required dependencies...")
    print("\nRun this command:")
    print("  pip install -r requirements.txt")
    print("\nOr install werkzeug directly:")
    print("  pip install werkzeug")
    print("\nThen run this script again:")
    print("  python3 generate_admin_hash.py")
    print("\n" + "="*60)
    sys.exit(1)

# Made with Bob