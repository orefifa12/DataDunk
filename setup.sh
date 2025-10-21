#!/bin/bash

echo "🏀 DataDunk NBA Database - Setup Script"
echo "========================================"

# Check if Docker is installed
echo "🔍 Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker Desktop"
    exit 1
fi

echo "✅ Docker found: $(docker --version)"

# Check if Python is installed
echo "🔍 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Start the database
echo ""
echo "🗄️ Starting PostgreSQL database..."
docker-compose up -d db

echo "⏳ Waiting for database to initialize..."
sleep 10

# Test database connection
echo "🔍 Testing database connection..."
if docker-compose exec db pg_isready -U nba_user -d nba_data; then
    echo "✅ Database is ready"
else
    echo "⚠️ Database might still be starting up. Try again in a few seconds."
fi

# Set up Python environment
echo ""
echo "🐍 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install psycopg2-binary

# Load sample data
echo ""
echo "📊 Loading sample data..."
python3 setup_for_team.py

echo ""
echo "✅ Setup complete! You can now:"
echo "  1. Run: python3 query_players.py"
echo "  2. Or connect directly to the database"
echo ""
echo "Database connection:"
echo "  Host: localhost, Port: 5432"
echo "  Database: nba_data, User: nba_user, Password: nba_password"
