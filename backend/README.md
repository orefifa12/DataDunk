# 🏀 DataDunk Backend

This directory contains all the backend components for the DataDunk NBA database system.

## 📁 Backend Structure

```
backend/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration for backend
├── init.sql                    # Database initialization script
├── database_setup.py           # Database schema and data loading
├── download_dataset.py         # NBA dataset downloader
├── query_players.py            # Interactive player query tool
├── sample_queries.py           # Sample query examples
├── test_database.py            # Database connection testing
├── manual_setup.py             # Manual setup instructions
├── setup_for_team.py           # Automated team setup script
└── player_queries.sql          # SQL query examples
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop
- Python 3.x

### Setup

```bash
# From the project root
cd backend

# Install dependencies
pip install -r requirements.txt

# Start database
docker-compose up -d db

# Test connection
python test_database.py
```

### Query Players

```bash
# Interactive queries
python query_players.py

# Direct SQL
psql -h localhost -p 5432 -U nba_user -d nba_data
```

## 🗄️ Database Configuration

- **Host**: localhost
- **Port**: 5432
- **Database**: nba_data
- **Username**: nba_user
- **Password**: nba_password

## 📊 Available Scripts

### Core Scripts

- `database_setup.py` - Set up database schema and load data
- `download_dataset.py` - Download NBA dataset from Kaggle
- `query_players.py` - Interactive player query interface

### Utility Scripts

- `test_database.py` - Test database connection and functionality
- `sample_queries.py` - Example queries and demonstrations
- `setup_for_team.py` - Automated setup for team members

### SQL Files

- `init.sql` - Database initialization
- `player_queries.sql` - SQL query examples

## 🔧 Development

### Adding New Queries

1. Add SQL queries to `player_queries.sql`
2. Add Python functions to `query_players.py`
3. Test with `test_database.py`

### Database Schema

The database uses a flexible JSONB structure:

- `nba_data` table with `data` JSONB column
- Indexed for performance
- Supports various NBA data formats

## 🐳 Docker

The backend can be run in Docker:

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs backend
```

## 📚 Documentation

- See main project README.md for complete setup instructions
- Check `../SETUP.md` for detailed setup guide
- Review `../TEAM_INSTRUCTIONS.md` for team collaboration
