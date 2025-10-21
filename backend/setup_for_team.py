#!/usr/bin/env python3
"""
Team Setup Script for DataDunk NBA Database
Run this script to set up the NBA database for your team.
"""

import subprocess
import sys
import os
import time

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_docker():
    """Check if Docker is running."""
    print("🔍 Checking Docker...")
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker is available: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker not found. Please install Docker Desktop")
            return False
    except FileNotFoundError:
        print("❌ Docker not found. Please install Docker Desktop")
        return False

def setup_database():
    """Set up the PostgreSQL database."""
    print("\n🗄️ Setting up NBA Database...")
    
    # Start the database
    if not run_command("docker-compose up -d db", "Starting PostgreSQL database"):
        return False
    
    # Wait for database to be ready
    print("⏳ Waiting for database to initialize...")
    time.sleep(10)
    
    # Test database connection
    if not run_command("docker-compose exec db pg_isready -U nba_user -d nba_data", "Testing database connection"):
        print("⚠️ Database might still be starting up. Try again in a few seconds.")
        return False
    
    return True

def setup_python_environment():
    """Set up Python virtual environment and dependencies."""
    print("\n🐍 Setting up Python environment...")
    
    # Create virtual environment
    if not run_command("python3 -m venv venv", "Creating virtual environment"):
        return False
    
    # Install dependencies
    if not run_command("source venv/bin/activate && pip install psycopg2-binary", "Installing Python dependencies"):
        return False
    
    return True

def load_sample_data():
    """Load sample NBA data for testing."""
    print("\n📊 Loading sample NBA data...")
    
    sample_data_script = '''
import psycopg2
import json

# Connect to database
conn = psycopg2.connect(host="localhost", port=5432, database="nba_data", user="nba_user", password="nba_password")
cursor = conn.cursor()

# Sample NBA players
sample_players = [
    {"player": "LeBron James", "team": "Lakers", "season": "2022-23", "pos": "SF", "pts": 28.9},
    {"player": "Stephen Curry", "team": "Warriors", "season": "2022-23", "pos": "PG", "pts": 29.4},
    {"player": "Kevin Durant", "team": "Suns", "season": "2022-23", "pos": "SF", "pts": 29.1},
    {"player": "Giannis Antetokounmpo", "team": "Bucks", "season": "2022-23", "pos": "PF", "pts": 31.1},
    {"player": "Luka Doncic", "team": "Mavericks", "season": "2022-23", "pos": "PG", "pts": 32.4},
    {"player": "Jayson Tatum", "team": "Celtics", "season": "2022-23", "pos": "SF", "pts": 30.1},
    {"player": "Joel Embiid", "team": "76ers", "season": "2022-23", "pos": "C", "pts": 33.1},
    {"player": "Nikola Jokic", "team": "Nuggets", "season": "2022-23", "pos": "C", "pts": 24.5}
]

print("Loading sample players...")
for player in sample_players:
    cursor.execute("INSERT INTO nba_data (table_name, data) VALUES (%s, %s)", ("sample_players", json.dumps(player)))

conn.commit()
print(f"✅ Loaded {len(sample_players)} sample players")
conn.close()
'''
    
    # Write the script to a temporary file
    with open('temp_load_data.py', 'w') as f:
        f.write(sample_data_script)
    
    # Run the script
    success = run_command("source venv/bin/activate && python3 temp_load_data.py", "Loading sample data")
    
    # Clean up
    if os.path.exists('temp_load_data.py'):
        os.remove('temp_load_data.py')
    
    return success

def test_setup():
    """Test the setup by running queries."""
    print("\n🧪 Testing the setup...")
    
    test_script = '''
import psycopg2

# Connect to database
conn = psycopg2.connect(host="localhost", port=5432, database="nba_data", user="nba_user", password="nba_password")
cursor = conn.cursor()

# Test query
cursor.execute("SELECT COUNT(*) FROM nba_data")
count = cursor.fetchone()[0]
print(f"✅ Database has {count} records")

# Get player names
cursor.execute("SELECT DISTINCT data->>'player' as player_name FROM nba_data WHERE data->>'player' IS NOT NULL")
players = cursor.fetchall()
print(f"✅ Found {len(players)} unique players:")
for player in players[:5]:  # Show first 5
    print(f"  • {player[0]}")

conn.close()
print("✅ Setup test completed successfully!")
'''
    
    # Write the test script
    with open('temp_test.py', 'w') as f:
        f.write(test_script)
    
    # Run the test
    success = run_command("source venv/bin/activate && python3 temp_test.py", "Testing database setup")
    
    # Clean up
    if os.path.exists('temp_test.py'):
        os.remove('temp_test.py')
    
    return success

def main():
    """Main setup function."""
    print("🏀 DataDunk NBA Database - Team Setup")
    print("=" * 50)
    
    # Check Docker
    if not check_docker():
        print("\n❌ Setup failed: Docker is required")
        print("Please install Docker Desktop and try again.")
        return
    
    # Setup database
    if not setup_database():
        print("\n❌ Setup failed: Could not start database")
        return
    
    # Setup Python environment
    if not setup_python_environment():
        print("\n❌ Setup failed: Could not set up Python environment")
        return
    
    # Load sample data
    if not load_sample_data():
        print("\n❌ Setup failed: Could not load sample data")
        return
    
    # Test setup
    if not test_setup():
        print("\n❌ Setup failed: Database test failed")
        return
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("=" * 50)
    print("\n📋 Next steps:")
    print("1. Query players: python3 query_players.py")
    print("2. Run SQL queries: psql -h localhost -p 5432 -U nba_user -d nba_data")
    print("3. Check QUICK_START.md for more examples")
    print("\n🔗 Database connection:")
    print("   Host: localhost, Port: 5432")
    print("   Database: nba_data, User: nba_user, Password: nba_password")

if __name__ == "__main__":
    main()
