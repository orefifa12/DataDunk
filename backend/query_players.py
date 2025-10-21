#!/usr/bin/env python3
"""
NBA Player Query Examples
Shows different ways to query player names and data.
"""

import psycopg2
import json

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
        print("✅ Connected to NBA database")
        return conn
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return None

def query_all_player_names(conn):
    """Query all player names from the database."""
    cursor = conn.cursor()
    
    # First, let's see what tables we have
    cursor.execute("""
        SELECT DISTINCT table_name 
        FROM nba_data 
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    print("📊 Available data tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Query for player names (assuming they're in JSON data)
    query = """
    SELECT DISTINCT 
        data->>'player' as player_name,
        data->>'team' as team,
        data->>'season' as season
    FROM nba_data 
    WHERE data->>'player' IS NOT NULL
    AND data->>'player' != ''
    ORDER BY player_name;
    """
    
    cursor.execute(query)
    players = cursor.fetchall()
    
    print(f"\n🏀 Found {len(players)} unique players:")
    print("=" * 50)
    
    for i, player in enumerate(players[:20]):  # Show first 20
        print(f"{i+1:2d}. {player[0]} - {player[1]} ({player[2]})")
    
    if len(players) > 20:
        print(f"... and {len(players) - 20} more players")
    
    return players

def search_players_by_name(conn, search_term):
    """Search for players by name."""
    cursor = conn.cursor()
    
    query = """
    SELECT DISTINCT 
        data->>'player' as player_name,
        data->>'team' as team,
        data->>'season' as season,
        data->>'pos' as position
    FROM nba_data 
    WHERE LOWER(data->>'player') LIKE LOWER(%s)
    ORDER BY player_name;
    """
    
    cursor.execute(query, (f'%{search_term}%',))
    players = cursor.fetchall()
    
    print(f"\n🔍 Players matching '{search_term}':")
    print("=" * 50)
    
    if players:
        for player in players:
            print(f"  • {player[0]} - {player[1]} ({player[2]}) - {player[3]}")
    else:
        print("  No players found matching that name.")
    
    return players

def get_players_by_team(conn, team_name):
    """Get all players from a specific team."""
    cursor = conn.cursor()
    
    query = """
    SELECT DISTINCT 
        data->>'player' as player_name,
        data->>'pos' as position,
        data->>'season' as season
    FROM nba_data 
    WHERE LOWER(data->>'team') LIKE LOWER(%s)
    ORDER BY player_name;
    """
    
    cursor.execute(query, (f'%{team_name}%',))
    players = cursor.fetchall()
    
    print(f"\n🏆 Players from {team_name}:")
    print("=" * 50)
    
    if players:
        for player in players:
            print(f"  • {player[0]} - {player[1]} ({player[2]})")
    else:
        print(f"  No players found for team: {team_name}")
    
    return players

def get_top_scorers(conn, limit=10):
    """Get top scoring players."""
    cursor = conn.cursor()
    
    query = """
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
    LIMIT %s;
    """
    
    cursor.execute(query, (limit,))
    players = cursor.fetchall()
    
    print(f"\n🔥 Top {limit} Scorers:")
    print("=" * 50)
    
    for i, player in enumerate(players, 1):
        print(f"{i:2d}. {player[0]} - {player[1]} - {player[2]} pts ({player[3]})")
    
    return players

def main():
    """Main function to demonstrate player queries."""
    print("🏀 NBA Player Query Examples")
    print("=" * 40)
    
    # Connect to database
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        # Query all player names
        all_players = query_all_player_names(conn)
        
        # Interactive search
        print("\n" + "="*50)
        print("🎯 Interactive Player Search")
        print("="*50)
        
        # Search for a specific player
        search_term = input("\nEnter a player name to search (or press Enter to skip): ").strip()
        if search_term:
            search_players_by_name(conn, search_term)
        
        # Search by team
        team_name = input("\nEnter a team name to search (or press Enter to skip): ").strip()
        if team_name:
            get_players_by_team(conn, team_name)
        
        # Show top scorers
        get_top_scorers(conn)
        
        print("\n✅ Query examples complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
