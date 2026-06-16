-- ============================================
-- SQL Script to Add World Cup 2026 Matches
-- Run this in pgAdmin Query Tool
-- ============================================

-- First, check if matches already exist
SELECT COUNT(*) as existing_matches FROM match;

-- Optional: Delete all existing matches (uncomment if needed)
-- DELETE FROM prediction;  -- Delete predictions first (foreign key constraint)
-- DELETE FROM match;       -- Then delete matches

-- ============================================
-- INSERT ALL MATCHES
-- ============================================

-- Group Stage Matches (72 matches)
INSERT INTO match (team_home, team_away, match_date, stage, is_finished) VALUES
('Mexico', 'South Africa', '2026-06-12 00:30:00', 'Group Stage', false),
('South Korea', 'Czechia', '2026-06-12 07:30:00', 'Group Stage', false),
('Canada', 'Bosnia and Herzegovina', '2026-06-13 00:30:00', 'Group Stage', false),
('USA', 'Paraguay', '2026-06-14 06:30:00', 'Group Stage', false),
('Qatar', 'Switzerland', '2026-06-14 00:30:00', 'Group Stage', false),
('Brazil', 'Morocco', '2026-06-14 03:30:00', 'Group Stage', false),
('Haiti', 'Scotland', '2026-06-14 06:30:00', 'Group Stage', false),
('Australia', 'Turkey', '2026-06-14 09:30:00', 'Group Stage', false),
('Germany', 'Curacao', '2026-06-14 22:30:00', 'Group Stage', false),
('Netherlands', 'Japan', '2026-06-15 01:30:00', 'Group Stage', false),
('Ivory Coast', 'Ecuador', '2026-06-15 04:30:00', 'Group Stage', false),
('Sweden', 'Tunisia', '2026-06-15 07:30:00', 'Group Stage', false),
('Spain', 'Cape Verde', '2026-06-15 21:30:00', 'Group Stage', false),
('Belgium', 'Egypt', '2026-06-16 00:30:00', 'Group Stage', false),
('Saudi Arabia', 'Uruguay', '2026-06-16 03:30:00', 'Group Stage', false),
('Iran', 'New Zealand', '2026-06-16 06:30:00', 'Group Stage', false),
('France', 'Senegal', '2026-06-17 00:30:00', 'Group Stage', false),
('Iraq', 'Norway', '2026-06-17 03:30:00', 'Group Stage', false),
('Argentina', 'Algeria', '2026-06-17 06:30:00', 'Group Stage', false),
('Austria', 'Jordan', '2026-06-17 09:30:00', 'Group Stage', false),
('Portugal', 'DR Congo', '2026-06-17 22:30:00', 'Group Stage', false),
('England', 'Croatia', '2026-06-18 01:30:00', 'Group Stage', false),
('Ghana', 'Panama', '2026-06-18 04:30:00', 'Group Stage', false),
('Uzbekistan', 'Colombia', '2026-06-18 07:30:00', 'Group Stage', false),
('Czechia', 'South Africa', '2026-06-18 21:30:00', 'Group Stage', false),
('Switzerland', 'Bosnia and Herzegovina', '2026-06-19 00:30:00', 'Group Stage', false),
('Canada', 'Qatar', '2026-06-19 03:30:00', 'Group Stage', false),
('Mexico', 'South Korea', '2026-06-19 06:30:00', 'Group Stage', false),
('USA', 'Australia', '2026-06-20 00:30:00', 'Group Stage', false),
('Scotland', 'Morocco', '2026-06-20 03:30:00', 'Group Stage', false),
('Brazil', 'Haiti', '2026-06-20 06:30:00', 'Group Stage', false),
('Turkey', 'Paraguay', '2026-06-20 09:30:00', 'Group Stage', false),
('Netherlands', 'Sweden', '2026-06-20 22:30:00', 'Group Stage', false),
('Germany', 'Ivory Coast', '2026-06-21 01:30:00', 'Group Stage', false),
('Ecuador', 'Curacao', '2026-06-21 05:30:00', 'Group Stage', false),
('Tunisia', 'Japan', '2026-06-21 09:30:00', 'Group Stage', false),
('Spain', 'Saudi Arabia', '2026-06-21 21:30:00', 'Group Stage', false),
('Belgium', 'Iran', '2026-06-22 00:30:00', 'Group Stage', false),
('Uruguay', 'Cape Verde', '2026-06-22 03:30:00', 'Group Stage', false),
('New Zealand', 'Egypt', '2026-06-22 06:30:00', 'Group Stage', false),
('Argentina', 'Austria', '2026-06-22 22:30:00', 'Group Stage', false),
('France', 'Iraq', '2026-06-23 02:30:00', 'Group Stage', false),
('Norway', 'Senegal', '2026-06-23 05:30:00', 'Group Stage', false),
('Jordan', 'Algeria', '2026-06-23 08:30:00', 'Group Stage', false),
('Portugal', 'Uzbekistan', '2026-06-23 22:30:00', 'Group Stage', false),
('England', 'Ghana', '2026-06-24 01:30:00', 'Group Stage', false),
('Panama', 'Croatia', '2026-06-24 04:30:00', 'Group Stage', false),
('Colombia', 'DR Congo', '2026-06-24 07:30:00', 'Group Stage', false),
('Switzerland', 'Canada', '2026-06-25 00:30:00', 'Group Stage', false),
('Bosnia and Herzegovina', 'Qatar', '2026-06-25 00:30:00', 'Group Stage', false),
('Morocco', 'Haiti', '2026-06-25 03:30:00', 'Group Stage', false),
('Scotland', 'Brazil', '2026-06-25 03:30:00', 'Group Stage', false),
('South Africa', 'South Korea', '2026-06-25 06:30:00', 'Group Stage', false),
('Czechia', 'Mexico', '2026-06-25 06:30:00', 'Group Stage', false),
('Curacao', 'Ivory Coast', '2026-06-26 01:30:00', 'Group Stage', false),
('Ecuador', 'Germany', '2026-06-26 01:30:00', 'Group Stage', false),
('Tunisia', 'Netherlands', '2026-06-26 04:30:00', 'Group Stage', false),
('Japan', 'Sweden', '2026-06-26 04:30:00', 'Group Stage', false),
('Turkey', 'USA', '2026-06-26 07:30:00', 'Group Stage', false),
('Paraguay', 'Australia', '2026-06-26 07:30:00', 'Group Stage', false),
('Norway', 'France', '2026-06-27 00:30:00', 'Group Stage', false),
('Senegal', 'Iraq', '2026-06-27 00:30:00', 'Group Stage', false),
('Cape Verde', 'Saudi Arabia', '2026-06-27 05:30:00', 'Group Stage', false),
('Uruguay', 'Spain', '2026-06-27 05:30:00', 'Group Stage', false),
('New Zealand', 'Belgium', '2026-06-27 08:30:00', 'Group Stage', false),
('Egypt', 'Iran', '2026-06-27 08:30:00', 'Group Stage', false),
('Panama', 'England', '2026-06-28 02:30:00', 'Group Stage', false),
('Croatia', 'Ghana', '2026-06-28 02:30:00', 'Group Stage', false),
('Colombia', 'Portugal', '2026-06-28 05:00:00', 'Group Stage', false),
('DR Congo', 'Uzbekistan', '2026-06-28 05:00:00', 'Group Stage', false),
('Algeria', 'Austria', '2026-06-28 07:30:00', 'Group Stage', false),
('Jordan', 'Argentina', '2026-06-28 07:30:00', 'Group Stage', false);

-- Round of 32 (16 matches)
INSERT INTO match (team_home, team_away, match_date, stage, is_finished) VALUES
('TBD', 'TBD', '2026-06-29 00:30:00', 'Round of 32', false),
('TBD', 'TBD', '2026-06-29 22:30:00', 'Round of 32', false),
('TBD', 'TBD', '2026-06-30 02:00:00', 'Round of 32', false),
('TBD', 'TBD', '2026-06-30 06:30:00', 'Round of 32', false),
('TBD', 'TBD', '2026-06-30 22:30:00', 'Round of 32', false),
('TBD', 'TBD', '2026-07-01 02:30:00', 'Round of 32', false),
('TBD', 'TBD', '2026-07-01 06:30:00', 'Round of 32', false),
('TBD', 'TBD', '2026-07-01 21:30:00', 'Round of 32', false),
('TBD', 'TBD', '2026-07-02 01:30:00', 'Round of 32', false),
('TBD', 'TBD', '2026-07-02 05:30:00', 'Round of 32', false),
('TBD', 'TBD', '2026-07-03 00:30:00', 'Round of 32', false),
('TBD', 'TBD', '2026-07-03 04:30:00', 'Round of 32', false),
('TBD', 'TBD', '2026-07-03 08:30:00', 'Round of 32', false),
('TBD', 'TBD', '2026-07-03 23:30:00', 'Round of 32', false),
('TBD', 'TBD', '2026-07-04 03:30:00', 'Round of 32', false),
('TBD', 'TBD', '2026-07-04 07:00:00', 'Round of 32', false);

-- Round of 16 (8 matches)
INSERT INTO match (team_home, team_away, match_date, stage, is_finished) VALUES
('TBD', 'TBD', '2026-07-04 10:30:00', 'Round of 16', false),
('TBD', 'TBD', '2026-07-05 02:30:00', 'Round of 16', false),
('TBD', 'TBD', '2026-07-06 01:30:00', 'Round of 16', false),
('TBD', 'TBD', '2026-07-06 05:30:00', 'Round of 16', false),
('TBD', 'TBD', '2026-07-07 00:30:00', 'Round of 16', false),
('TBD', 'TBD', '2026-07-07 05:30:00', 'Round of 16', false),
('TBD', 'TBD', '2026-07-07 21:30:00', 'Round of 16', false),
('TBD', 'TBD', '2026-07-08 01:30:00', 'Round of 16', false);

-- Quarter Finals (4 matches)
INSERT INTO match (team_home, team_away, match_date, stage, is_finished) VALUES
('TBD', 'TBD', '2026-07-10 01:30:00', 'Quarter Final', false),
('TBD', 'TBD', '2026-07-11 00:30:00', 'Quarter Final', false),
('TBD', 'TBD', '2026-07-12 02:30:00', 'Quarter Final', false),
('TBD', 'TBD', '2026-07-12 06:30:00', 'Quarter Final', false);

-- Semi Finals (2 matches)
INSERT INTO match (team_home, team_away, match_date, stage, is_finished) VALUES
('TBD', 'TBD', '2026-07-15 00:30:00', 'Semi Final', false),
('TBD', 'TBD', '2026-07-16 00:30:00', 'Semi Final', false);

-- Third Place (1 match)
INSERT INTO match (team_home, team_away, match_date, stage, is_finished) VALUES
('TBD', 'TBD', '2026-07-19 02:30:00', 'Third Place', false);

-- Final (1 match)
INSERT INTO match (team_home, team_away, match_date, stage, is_finished) VALUES
('TBD', 'TBD', '2026-07-20 00:30:00', 'Final', false);

-- ============================================
-- VERIFY THE INSERT
-- ============================================

-- Check total matches added
SELECT COUNT(*) as total_matches FROM match;

-- Check matches by stage
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

-- Show first 10 matches
SELECT id, team_home, team_away, match_date, stage 
FROM match 
ORDER BY match_date 
LIMIT 10;

-- ============================================
-- Expected Results:
-- Total: 119 matches
-- - Group Stage: 72
-- - Round of 32: 16
-- - Round of 16: 8
-- - Quarter Final: 4
-- - Semi Final: 2
-- - Third Place: 1
-- - Final: 1
-- ============================================

-- Made with Bob
