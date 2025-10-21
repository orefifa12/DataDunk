#!/usr/bin/env python3
"""
Manual Setup Script for NBA Database
Run this if Docker is having issues.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install Python requirements."""
    print("📦 Installing Python requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    return True

def check_postgresql():
    """Check if PostgreSQL is available."""
    print("🔍 Checking for PostgreSQL...")
    try:
        # Try to import psycopg2
        import psycopg2
        print("✅ psycopg2 is available")
        return True
    except ImportError:
        print("❌ psycopg2 not found. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "psycopg2-binary"], check=True)
            print("✅ psycopg2 installed")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install psycopg2")
            return False

def download_and_process_data():
    """Download and process the NBA dataset."""
    print("📥 Downloading NBA dataset...")
    try:
        from download_dataset import main as download_main
        download_main()
        print("✅ Dataset downloaded and processed")
        return True
    except Exception as e:
        print(f"❌ Failed to download dataset: {e}")
        return False

def setup_database_manually():
    """Provide instructions for manual database setup."""
    print("\n" + "="*60)
    print("🗄️  MANUAL DATABASE SETUP INSTRUCTIONS")
    print("="*60)
    print("""
Since Docker is having issues, here are your options:

1. **Install PostgreSQL locally:**
   - macOS: brew install postgresql
   - Start: brew services start postgresql
   - Create database: createdb nba_data

2. **Use a cloud database:**
   - PostgreSQL on AWS RDS, Google Cloud SQL, or Azure
   - Update connection details in database_setup.py

3. **Use a different Docker setup:**
   - Try: docker run -d --name nba-postgres -e POSTGRES_USER=nba_user -e POSTGRES_PASSWORD=nba_password -e POSTGRES_DB=nba_data -p 5432:5432 postgres:15

4. **Use SQLite instead:**
   - I can modify the scripts to use SQLite (no server needed)
""")

def main():
    """Main setup function."""
    print("🏀 NBA Database Manual Setup")
    print("="*40)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Check PostgreSQL
    if not check_postgresql():
        setup_database_manually()
        return
    
    # Download data
    if not download_and_process_data():
        return
    
    print("\n✅ Manual setup complete!")
    print("\nNext steps:")
    print("1. Set up a PostgreSQL database")
    print("2. Update database_setup.py with your connection details")
    print("3. Run: python database_setup.py")

if __name__ == "__main__":
    main()
