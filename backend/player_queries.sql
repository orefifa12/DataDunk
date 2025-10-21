-- NBA Player Query Examples
-- These are SQL queries you can run directly in the database

-- 1. Get all unique player names
SELECT DISTINCT 
    data->>'player' as player_name,
    data->>'team' as team,
    data->>'season' as season
FROM nba_data 
WHERE data->>'player' IS NOT NULL
AND data->>'player' != ''
ORDER BY player_name;

-- 2. Search for a specific player (replace 'LeBron' with any name)
SELECT DISTINCT 
    data->>'player' as player_name,
    data->>'team' as team,
    data->>'season' as season,
    data->>'pos' as position
FROM nba_data 
WHERE LOWER(data->>'player') LIKE LOWER('%LeBron%')
ORDER BY player_name;

-- 3. Get all players from a specific team (replace 'Lakers' with any team)
SELECT DISTINCT 
    data->>'player' as player_name,
    data->>'pos' as position,
    data->>'season' as season
FROM nba_data 
WHERE LOWER(data->>'team') LIKE LOWER('%Lakers%')
ORDER BY player_name;

-- 4. Get top scoring players
SELECT 
    data->>'player' as player_name,
    data->>'team' as team,
    data->>'pts' as points,
    data->>'season' as season
FROM nba_data 
WHERE data->>'pts' IS NOT NULL
AND data->>'pts' != ''
AND (data->>'pts')::numeric > 0
ORDER BY (data->>'pts')::numeric DESC
LIMIT 20;

-- 5. Get players by position
SELECT DISTINCT 
    data->>'player' as player_name,
    data->>'team' as team,
    data->>'pos' as position
FROM nba_data 
WHERE data->>'pos' = 'PG'  -- Replace 'PG' with any position
ORDER BY player_name;

-- 6. Get players from a specific season
SELECT DISTINCT 
    data->>'player' as player_name,
    data->>'team' as team,
    data->>'pos' as position
FROM nba_data 
WHERE data->>'season' = '2022-23'  -- Replace with any season
ORDER BY player_name;

-- 7. Count players by team
SELECT 
    data->>'team' as team,
    COUNT(DISTINCT data->>'player') as player_count
FROM nba_data 
WHERE data->>'team' IS NOT NULL
GROUP BY data->>'team'
ORDER BY player_count DESC;

-- 8. Get all available seasons
SELECT DISTINCT 
    data->>'season' as season
FROM nba_data 
WHERE data->>'season' IS NOT NULL
ORDER BY season;

-- 9. Get all available teams
SELECT DISTINCT 
    data->>'team' as team
FROM nba_data 
WHERE data->>'team' IS NOT NULL
ORDER BY team;

-- 10. Get all available positions
SELECT DISTINCT 
    data->>'pos' as position
FROM nba_data 
WHERE data->>'pos' IS NOT NULL
ORDER BY position;
