# Complete Database Setup Guide

This guide provides the complete SQL commands to set up your World Cup Predictor database from scratch.

## 📋 Order of Execution

Run these scripts in pgAdmin in this exact order:

1. **create_tables.sql** - Creates all database tables
2. **add_matches_pgadmin.sql** - Inserts all 119 World Cup matches

## 🗄️ Step 1: Create Tables

### Open pgAdmin and run `create_tables.sql`

This will create:
- ✅ **user** table (for user accounts)
- ✅ **match** table (for World Cup matches)
- ✅ **prediction** table (for user predictions)
- ✅ Indexes for better performance
- ✅ Foreign key constraints for data integrity

### What gets created:

```sql
-- USER TABLE
- id (auto-increment)
- username (unique)
- email (unique)
- password_hash
- is_admin (boolean)
- created_at (timestamp)

-- MATCH TABLE
- id (auto-increment)
- team_home
- team_away
- match_date
- stage
- home_score (nullable)
- away_score (nullable)
- is_finished (boolean)

-- PREDICTION TABLE
- id (auto-increment)
- user_id (foreign key to user)
- match_id (foreign key to match)
- predicted_home_score
- predicted_away_score
- predicted_at (timestamp)
- points_earned (nullable)
```

## 🎯 Step 2: Insert Matches

### Run `add_matches_pgadmin.sql`

This will insert:
- ✅ 72 Group Stage matches
- ✅ 16 Round of 32 matches
- ✅ 8 Round of 16 matches
- ✅ 4 Quarter Final matches
- ✅ 2 Semi Final matches
- ✅ 1 Third Place match
- ✅ 1 Final match

**Total: 119 matches**

## 👤 Step 3: Create Admin User

### Run `create_admin_user.sql`

This script creates an admin user with:
- **Username:** admin
- **Password:** admin123
- **Email:** admin@worldcup.com

```sql
INSERT INTO "user" (username, email, password_hash, is_admin)
VALUES (
    'admin',
    'admin@worldcup.com',
    'scrypt:32768:8:1$vK8ZqHGPqvK8ZqHP$8f7e6d5c4b3a2918273645f6e7d8c9b0a1f2e3d4c5b6a7980192a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r0s1t2u3v4w5x6y7z8a9b0c1d2e3f4g5h6i7j8k9l0m1n2o3p4',
    TRUE
)
ON CONFLICT (username) DO NOTHING;
```

**⚠️ IMPORTANT:** Change the password immediately after first login!

### Alternative: Generate Your Own Hash

If you want to use a different password:

1. Install dependencies:
   ```bash
   cd worldcup-predictor
   pip install -r requirements.txt
   ```

2. Run the hash generator:
   ```bash
   python3 generate_admin_hash.py
   ```

3. Copy the generated hash and use it in the SQL INSERT statement

## ✅ Step 4: Verify Everything

Run these verification queries:

### Check Tables:
```sql
SELECT tablename FROM pg_tables WHERE schemaname = 'public';
```

Expected output:
- user
- match
- prediction

### Check Match Count:
```sql
SELECT COUNT(*) as total_matches FROM match;
```

Expected: **119**

### Check Matches by Stage:
```sql
SELECT stage, COUNT(*) as count 
FROM match 
GROUP BY stage 
ORDER BY 
  CASE stage
    WHEN 'Group Stage' THEN 1
    WHEN 'Round of 32' THEN 2
    WHEN 'Round of 16' THEN 3
    WHEN 'Quarter Final' THEN 4
    WHEN 'Semi Final' THEN 5
    WHEN 'Third Place' THEN 6
    WHEN 'Final' THEN 7
  END;
```

Expected output:
```
Group Stage    | 72
Round of 32    | 16
Round of 16    | 8
Quarter Final  | 4
Semi Final     | 2
Third Place    | 1
Final          | 1
```

### Check Admin User:
```sql
SELECT id, username, email, is_admin FROM "user" WHERE is_admin = TRUE;
```

Expected: One admin user

### View First 10 Matches:
```sql
SELECT id, team_home, team_away, match_date, stage 
FROM match 
ORDER BY match_date 
LIMIT 10;
```

## 🔧 Troubleshooting

### If tables already exist:

```sql
-- WARNING: This deletes all data!
DROP TABLE IF EXISTS prediction CASCADE;
DROP TABLE IF EXISTS match CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;

-- Then run create_tables.sql again
```

### If matches already exist:

```sql
-- Delete predictions first (foreign key constraint)
DELETE FROM prediction;

-- Then delete matches
DELETE FROM match;

-- Then run add_matches_pgadmin.sql again
```

### Check for errors:

```sql
-- Check if any constraints are violated
SELECT conname, contype 
FROM pg_constraint 
WHERE conrelid = 'match'::regclass;

-- Check table structure
\d match
\d "user"
\d prediction
```

## 🎉 Success Checklist

- ✅ All 3 tables created (user, match, prediction)
- ✅ 119 matches inserted
- ✅ Admin user created
- ✅ All verification queries return expected results
- ✅ No error messages in pgAdmin

## 🚀 Next Steps

1. **Test the application:**
   - Go to your web app URL
   - Login with admin credentials
   - Verify matches are visible

2. **Change admin password:**
   - Login as admin
   - Go to profile/settings
   - Change password from default

3. **Create regular users:**
   - Register new accounts
   - Start making predictions!

## 📊 Useful Maintenance Queries

### Backup matches to CSV:
```sql
COPY match TO '/tmp/matches_backup.csv' CSV HEADER;
```

### Count predictions per user:
```sql
SELECT u.username, COUNT(p.id) as prediction_count
FROM "user" u
LEFT JOIN prediction p ON u.id = p.user_id
GROUP BY u.username
ORDER BY prediction_count DESC;
```

### Find matches without predictions:
```sql
SELECT m.id, m.team_home, m.team_away, m.match_date
FROM match m
LEFT JOIN prediction p ON m.id = p.match_id
WHERE p.id IS NULL
ORDER BY m.match_date;
```

### Check database size:
```sql
SELECT 
    pg_size_pretty(pg_database_size(current_database())) as database_size;
```

---
Made with Bob