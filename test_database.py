#!/usr/bin/env python3
"""
Simple Database Test Script
Tests both SQLite and PostgreSQL connections.
"""

import sqlite3
import os
import sys

def test_sqlite():
    """Test SQLite database creation and basic operations."""
    print("🧪 Testing SQLite Database...")
    
    try:
        # Create SQLite database
        conn = sqlite3.connect('test_nba.db')
        cursor = conn.cursor()
        
        # Create a test table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_players (
                id INTEGER PRIMARY KEY,
                name TEXT,
                points INTEGER,
                team TEXT
            )
        ''')
        
        # Insert test data
        test_data = [
            ('LeBron James', 25, 'Lakers'),
            ('Stephen Curry', 30, 'Warriors'),
            ('Kevin Durant', 28, 'Suns')
        ]
        
        cursor.executemany('INSERT INTO test_players (name, points, team) VALUES (?, ?, ?)', test_data)
        conn.commit()
        
        # Query test data
        cursor.execute('SELECT * FROM test_players')
        results = cursor.fetchall()
        
        print("✅ SQLite test successful!")
        print("📊 Test data:")
        for row in results:
            print(f"  {row[1]} - {row[2]} points - {row[3]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ SQLite test failed: {e}")
        return False

def test_postgresql():
    """Test PostgreSQL connection if available."""
    print("\n🧪 Testing PostgreSQL Connection...")
    
    try:
        import psycopg2
        
        # Try to connect to local PostgreSQL
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='nba_data',
            user='nba_user',
            password='nba_password'
        )
        
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()
        
        print("✅ PostgreSQL connection successful!")
        print(f"📊 PostgreSQL version: {version[0]}")
        
        conn.close()
        return True
        
    except ImportError:
        print("⚠️  psycopg2 not installed. Install with: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def test_docker():
    """Test if Docker is working."""
    print("\n🧪 Testing Docker...")
    
    try:
        import subprocess
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is available")
            print(f"📊 Docker version: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker command failed")
            return False
    except FileNotFoundError:
        print("❌ Docker not found. Please install Docker")
        return False
    except Exception as e:
        print(f"❌ Docker test failed: {e}")
        return False

def test_python_environment():
    """Test Python environment and packages."""
    print("\n🧪 Testing Python Environment...")
    
    try:
        import pandas
        print("✅ pandas available")
    except ImportError:
        print("❌ pandas not available")
    
    try:
        import kagglehub
        print("✅ kagglehub available")
    except ImportError:
        print("❌ kagglehub not available")
    
    try:
        import psycopg2
        print("✅ psycopg2 available")
    except ImportError:
        print("❌ psycopg2 not available")

def main():
    """Run all tests."""
    print("🏀 NBA Database Test Suite")
    print("=" * 40)
    
    # Test Python environment
    test_python_environment()
    
    # Test SQLite (should always work)
    sqlite_works = test_sqlite()
    
    # Test Docker
    docker_works = test_docker()
    
    # Test PostgreSQL
    postgres_works = test_postgresql()
    
    print("\n" + "=" * 40)
    print("📋 Test Summary:")
    print(f"  SQLite: {'✅' if sqlite_works else '❌'}")
    print(f"  Docker: {'✅' if docker_works else '❌'}")
    print(f"  PostgreSQL: {'✅' if postgres_works else '❌'}")
    
    if sqlite_works:
        print("\n🎉 At least SQLite is working! You can use the SQLite version.")
    
    if docker_works and not postgres_works:
        print("\n💡 Docker is working but PostgreSQL isn't running. Try:")
        print("   docker-compose up -d db")
    
    if not docker_works:
        print("\n💡 Docker issues detected. Try:")
        print("   1. Restart Docker Desktop")
        print("   2. Use SQLite version instead")

if __name__ == "__main__":
    main()
