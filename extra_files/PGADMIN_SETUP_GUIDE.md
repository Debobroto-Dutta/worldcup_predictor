# pgAdmin Setup Guide - Add Matches to Database

This guide will walk you through connecting to your PostgreSQL database via pgAdmin and adding World Cup 2026 matches.

## 📋 Prerequisites

1. **pgAdmin installed** on your computer
   - Download from: https://www.pgadmin.org/download/
   - Or use the web version if available

2. **Database connection details** (from Render or your hosting provider):
   - Host/Server address
   - Port (usually 5432)
   - Database name
   - Username
   - Password

## 🔌 Step 1: Connect to Your Database

### Get Your Database Connection Details

#### If using Render.com:
1. Go to https://dashboard.render.com
2. Click on your PostgreSQL database
3. Find the "Connections" section
4. Copy the following details:
   - **Hostname** (e.g., `dpg-xxxxx.oregon-postgres.render.com`)
   - **Port** (usually `5432`)
   - **Database** (e.g., `worldcup_db`)
   - **Username** (e.g., `worldcup_user`)
   - **Password** (click "Copy" to get the password)

### Add Server in pgAdmin:

1. **Open pgAdmin**

2. **Right-click on "Servers"** in the left panel
   - Select **"Register" → "Server..."**

3. **General Tab:**
   - **Name:** `World Cup Predictor` (or any name you prefer)

4. **Connection Tab:**
   - **Host name/address:** Paste your hostname (e.g., `dpg-xxxxx.oregon-postgres.render.com`)
   - **Port:** `5432`
   - **Maintenance database:** `postgres` (default)
   - **Username:** Paste your database username
   - **Password:** Paste your database password
   - ✅ Check **"Save password"** (optional, for convenience)

5. **SSL Tab:**
   - **SSL mode:** `Require` (for Render and most cloud providers)

6. **Click "Save"**

### Verify Connection:

- You should see your server appear in the left panel
- Expand it to see: Databases → [Your Database Name] → Schemas → public → Tables
- You should see tables: `user`, `match`, `prediction`

## 📊 Step 2: Open Query Tool

1. **Navigate to your database:**
   - Servers → World Cup Predictor → Databases → [Your Database Name]

2. **Right-click on your database name**
   - Select **"Query Tool"**
   - A new query window will open

## 📝 Step 3: Run the SQL Script

### Option A: Copy and Paste

1. **Open the file:** `add_matches_pgadmin.sql` (in your project folder)

2. **Copy all contents** (Ctrl+A, Ctrl+C)

3. **Paste into pgAdmin Query Tool** (Ctrl+V)

4. **Click the Execute button** (▶️ icon) or press **F5**

5. **Wait for completion** (should take a few seconds)

### Option B: Open File Directly

1. In Query Tool, click **"Open File"** icon (📁)

2. Navigate to your project folder

3. Select **`add_matches_pgadmin.sql`**

4. Click **"Execute"** (▶️) or press **F5**

## ✅ Step 4: Verify the Results

After running the script, you should see output in the "Data Output" panel:

### Expected Results:

```
Query returned successfully in XXX msec.

existing_matches: 0 (or current count)

INSERT 0 119  (119 rows inserted)

total_matches: 119

stage              | count
-------------------+-------
Group Stage        | 72
Round of 32        | 16
Round of 16        | 8
Quarter Final      | 4
Semi Final         | 2
Third Place        | 1
Final              | 1
```

### View the Matches:

Run this query to see the first 10 matches:

```sql
SELECT id, team_home, team_away, match_date, stage 
FROM match 
ORDER BY match_date 
LIMIT 10;
```

## 🔍 Troubleshooting

### Connection Issues

**Error: "could not connect to server"**
- ✅ Check your hostname, port, username, and password
- ✅ Ensure SSL mode is set to "Require"
- ✅ Check if your IP is whitelisted (some providers require this)
- ✅ Verify the database is running (check Render dashboard)

**Error: "password authentication failed"**
- ✅ Copy the password again from Render (don't type it manually)
- ✅ Make sure there are no extra spaces

**Error: "SSL connection required"**
- ✅ Go to Connection → SSL tab
- ✅ Set SSL mode to "Require"

### Query Execution Issues

**Error: "relation 'match' does not exist"**
- ✅ Make sure you're connected to the correct database
- ✅ Run the database initialization first:
  ```sql
  -- Check if tables exist
  SELECT tablename FROM pg_tables WHERE schemaname = 'public';
  ```

**Error: "duplicate key value violates unique constraint"**
- Matches already exist in the database
- To delete and re-add:
  ```sql
  DELETE FROM prediction;  -- Delete predictions first
  DELETE FROM match;       -- Then delete matches
  -- Now run the insert script again
  ```

**Error: "permission denied"**
- ✅ Make sure you're using the correct database user
- ✅ Check if the user has INSERT permissions

## 🗑️ Optional: Clear Existing Matches

If you need to start fresh:

```sql
-- WARNING: This will delete all predictions and matches!

-- Step 1: Delete all predictions (must be done first due to foreign key)
DELETE FROM prediction;

-- Step 2: Delete all matches
DELETE FROM match;

-- Step 3: Verify deletion
SELECT COUNT(*) FROM match;  -- Should return 0

-- Step 4: Now run the insert script from add_matches_pgadmin.sql
```

## 📊 Useful Queries

### Check Total Matches:
```sql
SELECT COUNT(*) as total_matches FROM match;
```

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

### View Upcoming Matches:
```sql
SELECT id, team_home, team_away, match_date, stage 
FROM match 
WHERE match_date > NOW()
ORDER BY match_date 
LIMIT 20;
```

### Check if Database is Working:
```sql
-- Check all tables
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- Check user count
SELECT COUNT(*) FROM "user";

-- Check match count
SELECT COUNT(*) FROM match;

-- Check prediction count
SELECT COUNT(*) FROM prediction;
```

## 🎉 Success!

Once you see "119 matches" in your database:

1. **Refresh your web application**
2. **Login to your account**
3. **You should now see all World Cup 2026 matches!**
4. **Start making predictions!**

## 🔐 Security Tips

1. **Don't share your database credentials**
2. **Use strong passwords**
3. **Enable SSL connections**
4. **Regularly backup your database**
5. **Monitor database access logs**

## 📞 Need More Help?

- Check Render documentation: https://render.com/docs/databases
- pgAdmin documentation: https://www.pgadmin.org/docs/
- PostgreSQL documentation: https://www.postgresql.org/docs/

---
Made with Bob