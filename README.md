# 🏀 DataDunk NBA Database

**Team**: Data Dunk  
**Members**: Cyril Rikh, David Boham, John Park, Ethan Liao, Matias Gandarias  
**Project**: NBA Player Querying Service

Our project, Data Dunk, will design and implement a relational database system that takes basketball game, player, and team statistics, and exposes them through SQL queries and a simple front-end making it more accessible for the end user. At the end of the project, we will demonstrate a system that supports schema-based storage of games, players, teams, and statistics, and lets users run interesting and non-trivial queries over seasons of basketball data.

## 🚀 Quick Start for Team Members

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone <your-github-repo-url>
cd DataDunk

# Run the automated setup
python3 setup_for_team.py
```

### Option 2: Manual Setup

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

## 🎯 Query NBA Players

### Interactive Queries

```bash
# Run the player query script
python3 query_players.py
```

### Direct SQL Queries

```bash
# Connect to database
psql -h localhost -p 5432 -U nba_user -d nba_data

# Example queries
SELECT DISTINCT data->>'player' as player_name, data->>'team' as team
FROM nba_data
WHERE data->>'player' IS NOT NULL
ORDER BY player_name;
```

## 📊 Database Connection

- **Host**: localhost
- **Port**: 5432
- **Database**: nba_data
- **Username**: nba_user
- **Password**: nba_password

## 📚 Documentation

- `QUICK_START.md` - Quick setup guide
- `SETUP.md` - Detailed setup instructions
- `player_queries.sql` - SQL query examples
- `query_players.py` - Python query examples

## 🛠️ Troubleshooting

- **Docker issues?** Check `docker-compose logs db`
- **Python issues?** Make sure virtual environment is activated
- **Need help?** Check the documentation files above

---

_Utilizing the NBA database, we provide a querying service for users to access and find their desired players based on data._
