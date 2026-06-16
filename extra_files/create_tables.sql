-- ============================================
-- CREATE TABLES FOR WORLD CUP PREDICTOR
-- Run this FIRST before inserting matches
-- ============================================

-- Drop existing tables if they exist (optional - uncomment if needed)
-- DROP TABLE IF EXISTS prediction CASCADE;
-- DROP TABLE IF EXISTS match CASCADE;
-- DROP TABLE IF EXISTS "user" CASCADE;

-- ============================================
-- CREATE USER TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- CREATE MATCH TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS match (
    id SERIAL PRIMARY KEY,
    team_home VARCHAR(100) NOT NULL,
    team_away VARCHAR(100) NOT NULL,
    match_date TIMESTAMP NOT NULL,
    stage VARCHAR(50) NOT NULL,
    home_score INTEGER,
    away_score INTEGER,
    is_finished BOOLEAN DEFAULT FALSE
);

-- ============================================
-- CREATE PREDICTION TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS prediction (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    match_id INTEGER NOT NULL,
    predicted_home_score INTEGER NOT NULL,
    predicted_away_score INTEGER NOT NULL,
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    points_earned INTEGER,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE,
    CONSTRAINT fk_match FOREIGN KEY (match_id) REFERENCES match(id) ON DELETE CASCADE,
    CONSTRAINT _user_match_uc UNIQUE (user_id, match_id)
);

-- ============================================
-- CREATE INDEXES FOR BETTER PERFORMANCE
-- ============================================
CREATE INDEX IF NOT EXISTS idx_match_date ON match(match_date);
CREATE INDEX IF NOT EXISTS idx_match_stage ON match(stage);
CREATE INDEX IF NOT EXISTS idx_match_finished ON match(is_finished);
CREATE INDEX IF NOT EXISTS idx_prediction_user ON prediction(user_id);
CREATE INDEX IF NOT EXISTS idx_prediction_match ON prediction(match_id);
CREATE INDEX IF NOT EXISTS idx_user_username ON "user"(username);
CREATE INDEX IF NOT EXISTS idx_user_email ON "user"(email);

-- ============================================
-- CREATE DEFAULT ADMIN USER
-- Password: admin123 (hashed with werkzeug)
-- ============================================
INSERT INTO "user" (username, email, password_hash, is_admin)
VALUES (
    'admin',
    'admin@worldcup.com',
    'scrypt:32768:8:1$YourHashHere$...',  -- You'll need to generate this
    TRUE
)
ON CONFLICT (username) DO NOTHING;

-- ============================================
-- VERIFY TABLE CREATION
-- ============================================
SELECT 
    tablename, 
    schemaname 
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY tablename;

-- Check table structures
\d "user"
\d match
\d prediction

-- ============================================
-- NOTES:
-- 1. Run this script BEFORE running add_matches_pgadmin.sql
-- 2. The admin password hash needs to be generated properly
-- 3. All tables use SERIAL for auto-incrementing IDs
-- 4. Foreign keys ensure data integrity
-- 5. Indexes improve query performance
-- ============================================

-- ============================================
-- ALTERNATIVE: Generate Admin Password Hash
-- ============================================
-- If you need to create an admin user with a proper password hash,
-- you can use Python to generate it:
--
-- python3 -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('admin123'))"
--
-- Then update the INSERT statement above with the generated hash
-- ============================================

-- Made with Bob
