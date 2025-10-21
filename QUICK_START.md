# 🏀 DataDunk NBA Database - Quick Start Guide

## For Your Teammates: Get Started in 5 Minutes! ⚡

### Prerequisites

- Docker Desktop installed
- Git installed

### Step 1: Clone the Repository

```bash
git clone <your-github-repo-url>
cd DataDunk
```

### Step 2: Start the Database

```bash
# Start PostgreSQL database
docker-compose up -d db

# Wait a few seconds for database to initialize
```

### Step 3: Test the Connection

```bash
# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

# Test the database
python3 backend/test_database.py
```

### Step 4: Query Players! 🎯

```bash
# Interactive player queries
python3 backend/query_players.py

# Or run direct SQL queries
psql -h localhost -p 5432 -U nba_user -d nba_data
```

## Database Connection Details

- **Host**: localhost
- **Port**: 5432
- **Database**: nba_data
- **Username**: nba_user
- **Password**: nba_password

## Quick SQL Examples

```sql
-- Get all player names
SELECT DISTINCT data->>'player' as player_name, data->>'team' as team
FROM nba_data
WHERE data->>'player' IS NOT NULL
ORDER BY player_name;

-- Search for a specific player
SELECT data->>'player' as player_name, data->>'team' as team, data->>'pts' as points
FROM nba_data
WHERE LOWER(data->>'player') LIKE LOWER('%LeBron%');

-- Top scorers
SELECT data->>'player' as player_name, data->>'team' as team, data->>'pts' as points
FROM nba_data
WHERE data->>'pts' IS NOT NULL
ORDER BY (data->>'pts')::numeric DESC
LIMIT 10;
```

## Troubleshooting

- **Database not starting?** Run `docker-compose logs db`
- **Connection issues?** Make sure Docker is running
- **Python issues?** Make sure you're in the virtual environment

## Need Help?

Check the full `SETUP.md` file for detailed instructions!
