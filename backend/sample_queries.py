#!/usr/bin/env python3
"""
Sample Queries for NBA Database
Demonstrates how to query the NBA database and provides useful examples.
"""

import psycopg2
import pandas as pd
import json
from pathlib import Path

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'nba_data',
    'user': 'nba_user',
    'password': 'nba_password'
}

def connect_to_database():
    """Create a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Successfully connected to NBA database")
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        raise

def get_database_summary(conn):
    """Get a summary of all available data in the database."""
    query = """
    SELECT 
        table_name,
        COUNT(*) as record_count,
        MIN(created_at) as first_loaded,
        MAX(created_at) as last_updated
    FROM nba_data 
    GROUP BY table_name
    ORDER BY record_count DESC;
    """
    
    df = pd.read_sql(query, conn)
    print("\n📊 Database Summary:")
    print("=" * 50)
    print(df.to_string(index=False))
    return df

def find_top_scorers(conn, limit=10):
    """Find the top scoring players."""
    query = """
    SELECT 
        data->>'player' as player_name,
        data->>'pts' as points,
        data->>'season' as season,
        data->>'team' as team
    FROM nba_data 
    WHERE table_name LIKE '%player%' 
    AND data->>'pts' IS NOT NULL
    AND (data->>'pts')::numeric > 0
    ORDER BY (data->>'pts')::numeric DESC
    LIMIT %s;
    """
    
    df = pd.read_sql(query, conn, params=[limit])
    print(f"\n🏀 Top {limit} Scorers:")
    print("=" * 50)
    print(df.to_string(index=False))
    return df

def get_team_statistics(conn):
    """Get team statistics."""
    query = """
    SELECT 
        data->>'team' as team_name,
        COUNT(*) as games_played,
        AVG((data->>'pts')::numeric) as avg_points
    FROM nba_data 
    WHERE data->>'team' IS NOT NULL
    AND data->>'pts' IS NOT NULL
    AND (data->>'pts')::numeric > 0
    GROUP BY data->>'team'
    ORDER BY games_played DESC
    LIMIT 15;
    """
    
    df = pd.read_sql(query, conn)
    print("\n🏆 Team Statistics:")
    print("=" * 50)
    print(df.to_string(index=False))
    return df

def search_players_by_name(conn, player_name):
    """Search for a specific player."""
    query = """
    SELECT 
        data->>'player' as player_name,
        data->>'pts' as points,
        data->>'season' as season,
        data->>'team' as team,
        data->>'pos' as position
    FROM nba_data 
    WHERE LOWER(data->>'player') LIKE LOWER(%s)
    ORDER BY (data->>'pts')::numeric DESC
    LIMIT 20;
    """
    
    df = pd.read_sql(query, conn, params=[f'%{player_name}%'])
    print(f"\n🔍 Search Results for '{player_name}':")
    print("=" * 50)
    if len(df) > 0:
        print(df.to_string(index=False))
    else:
        print("No players found matching that name.")
    return df

def get_season_stats(conn, season):
    """Get statistics for a specific season."""
    query = """
    SELECT 
        data->>'player' as player_name,
        data->>'team' as team,
        data->>'pts' as points,
        data->>'reb' as rebounds,
        data->>'ast' as assists
    FROM nba_data 
    WHERE data->>'season' = %s
    AND data->>'pts' IS NOT NULL
    ORDER BY (data->>'pts')::numeric DESC
    LIMIT 20;
    """
    
    df = pd.read_sql(query, conn, params=[season])
    print(f"\n📅 {season} Season Top Performers:")
    print("=" * 50)
    print(df.to_string(index=False))
    return df

def explore_data_structure(conn, table_name=None):
    """Explore the structure of the data."""
    if table_name:
        query = """
        SELECT data
        FROM nba_data 
        WHERE table_name = %s
        LIMIT 1;
        """
        df = pd.read_sql(query, conn, params=[table_name])
    else:
        query = """
        SELECT data
        FROM nba_data 
        LIMIT 1;
        """
        df = pd.read_sql(query, conn)
    
    if len(df) > 0:
        sample_data = df['data'].iloc[0]
        print(f"\n🔍 Sample Data Structure:")
        print("=" * 50)
        print(json.dumps(sample_data, indent=2))
    else:
        print("No data found.")

def main():
    """Main function to demonstrate database queries."""
    try:
        # Connect to database
        conn = connect_to_database()
        
        # Get database summary
        get_database_summary(conn)
        
        # Find top scorers
        find_top_scorers(conn)
        
        # Get team statistics
        get_team_statistics(conn)
        
        # Explore data structure
        explore_data_structure(conn)
        
        # Interactive search
        print("\n" + "="*50)
        print("🎯 Interactive Queries")
        print("="*50)
        
        # Search for a specific player
        player_name = input("\nEnter a player name to search (or press Enter to skip): ").strip()
        if player_name:
            search_players_by_name(conn, player_name)
        
        # Get season stats
        season = input("\nEnter a season (e.g., '2022-23') or press Enter to skip: ").strip()
        if season:
            get_season_stats(conn, season)
        
        print("\n✅ Query demonstration complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
