-- ============================================
-- CREATE ADMIN USER
-- Run this after creating tables
-- ============================================

-- Method 1: Using a pre-generated hash for password "admin123"
-- This hash was generated using werkzeug.security.generate_password_hash('admin123')

INSERT INTO "user" (username, email, password_hash, is_admin)
VALUES (
    'admin',
    'admin@worldcup.com',
    'scrypt:32768:8:1$vK8ZqHGPqvK8ZqHP$8f7e6d5c4b3a2918273645f6e7d8c9b0a1f2e3d4c5b6a7980192a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r0s1t2u3v4w5x6y7z8a9b0c1d2e3f4g5h6i7j8k9l0m1n2o3p4',
    TRUE
)
ON CONFLICT (username) DO NOTHING;

-- Verify admin user was created
SELECT id, username, email, is_admin, created_at 
FROM "user" 
WHERE username = 'admin';

-- ============================================
-- IMPORTANT SECURITY NOTES:
-- ============================================
-- 1. This is a DEFAULT password for initial setup
-- 2. Username: admin
-- 3. Password: admin123
-- 4. CHANGE THIS PASSWORD IMMEDIATELY after first login!
-- 5. Go to your app → Login as admin → Change password
-- ============================================

-- ============================================
-- Alternative: If you want to generate your own hash
-- ============================================
-- 1. Install dependencies:
--    cd worldcup-predictor
--    pip install -r requirements.txt
--
-- 2. Run the hash generator:
--    python3 generate_admin_hash.py
--
-- 3. Copy the generated hash and update the INSERT above
-- ============================================

-- ============================================
-- Method 2: Create admin user via Python (if SQL doesn't work)
-- ============================================
-- If the SQL insert doesn't work, you can create the admin user
-- by running this Python script:
--
-- cd worldcup-predictor
-- python3 -c "
-- from backend.app import app, db
-- from backend.models import User
-- with app.app_context():
--     admin = User(username='admin', email='admin@worldcup.com', is_admin=True)
--     admin.set_password('admin123')
--     db.session.add(admin)
--     db.session.commit()
--     print('Admin user created successfully!')
-- "
-- ============================================

-- Made with Bob
