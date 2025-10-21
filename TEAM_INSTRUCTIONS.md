# 🏀 DataDunk NBA Database - Team Instructions

## For Your Teammates: How to Get Started

### Prerequisites

- Docker Desktop installed
- Git installed
- Python 3 installed

### Step 1: Clone the Repository

```bash
git clone <your-github-repo-url>
cd DataDunk
```

### Step 2: Choose Your Setup Method

#### Option A: Automated Setup (Easiest)

```bash
# For Mac/Linux
./setup.sh

# For Windows
setup_windows.bat

# Or use Python script (works on all platforms)
python3 setup_for_team.py
```

#### Option B: Manual Setup

```bash
# 1. Start the database
docker-compose up -d db

# 2. Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install psycopg2-binary

# 3. Test the setup
python3 test_database.py
```

### Step 3: Query NBA Players! 🎯

#### Interactive Python Queries

```bash
# Run the interactive player query script
python3 query_players.py
```

#### Direct SQL Queries

```bash
# Connect to database
psql -h localhost -p 5432 -U nba_user -d nba_data

# Example: Get all player names
SELECT DISTINCT data->>'player' as player_name, data->>'team' as team
FROM nba_data
WHERE data->>'player' IS NOT NULL
ORDER BY player_name;
```

#### Python Code Examples

```python
import psycopg2

# Connect to database
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='nba_data',
    user='nba_user',
    password='nba_password'
)

cursor = conn.cursor()

# Get all players
cursor.execute("""
    SELECT DISTINCT data->>'player' as player_name, data->>'team' as team
    FROM nba_data
    WHERE data->>'player' IS NOT NULL
    ORDER BY player_name
""")

players = cursor.fetchall()
for player in players:
    print(f"{player[0]} - {player[1]}")

conn.close()
```

## 📊 Database Connection Details

- **Host**: localhost
- **Port**: 5432
- **Database**: nba_data
- **Username**: nba_user
- **Password**: nba_password

## 🔍 Common Query Examples

### Get All Player Names

```sql
SELECT DISTINCT data->>'player' as player_name, data->>'team' as team
FROM nba_data
WHERE data->>'player' IS NOT NULL
ORDER BY player_name;
```

### Search for Specific Player

```sql
SELECT data->>'player' as player_name, data->>'team' as team, data->>'pts' as points
FROM nba_data
WHERE LOWER(data->>'player') LIKE LOWER('%LeBron%');
```

### Get Players by Team

```sql
SELECT data->>'player' as player_name, data->>'pos' as position
FROM nba_data
WHERE LOWER(data->>'team') LIKE LOWER('%Lakers%');
```

### Top Scorers

```sql
SELECT data->>'player' as player_name, data->>'team' as team, data->>'pts' as points
FROM nba_data
WHERE data->>'pts' IS NOT NULL
ORDER BY (data->>'pts')::numeric DESC
LIMIT 10;
```

## 🛠️ Troubleshooting

### Database Not Starting?

```bash
# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Python Issues?

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

# Check if psycopg2 is installed
pip list | grep psycopg2
```

### Connection Issues?

```bash
# Test database connection
python3 test_database.py

# Check if database is running
docker-compose ps
```

## 📚 Available Files

- `query_players.py` - Interactive Python queries
- `player_queries.sql` - SQL query examples
- `test_database.py` - Test database connection
- `setup_for_team.py` - Automated setup script
- `QUICK_START.md` - Quick setup guide
- `SETUP.md` - Detailed setup instructions

## 🎯 Quick Commands Summary

```bash
# Start database
docker-compose up -d db

# Query players interactively
python3 query_players.py

# Test database
python3 test_database.py

# Connect directly to database
psql -h localhost -p 5432 -U nba_user -d nba_data
```

## 🆘 Need Help?

1. Check the troubleshooting section above
2. Look at the documentation files
3. Ask your team members
4. Check Docker and Python installation

---

**Happy Querying! 🏀**
