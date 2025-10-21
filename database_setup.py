#!/usr/bin/env python3
"""
Database Setup and Data Loading Script
Creates the database schema and loads NBA data into PostgreSQL.
"""

import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import logging
from pathlib import Path
import glob

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'nba_data'),
    'user': os.getenv('DB_USER', 'nba_user'),
    'password': os.getenv('DB_PASSWORD', 'nba_password')
}

def create_connection():
    """Create a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info("Successfully connected to PostgreSQL database")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise

def create_tables(conn):
    """Create the database tables for NBA data."""
    cursor = conn.cursor()
    
    # Create a general NBA data table that can handle various CSV structures
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS nba_data (
        id SERIAL PRIMARY KEY,
        table_name VARCHAR(100),
        data JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create indexes for better query performance
    CREATE INDEX IF NOT EXISTS idx_nba_data_table_name ON nba_data(table_name);
    CREATE INDEX IF NOT EXISTS idx_nba_data_jsonb ON nba_data USING GIN(data);
    """
    
    try:
        cursor.execute(create_table_sql)
        conn.commit()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise
    finally:
        cursor.close()

def load_csv_to_database(conn, csv_file_path, table_name):
    """Load a CSV file into the database."""
    try:
        logger.info(f"Loading {csv_file_path} into database...")
        
        # Read CSV file
        df = pd.read_csv(csv_file_path)
        
        # Convert DataFrame to list of dictionaries
        records = df.to_dict('records')
        
        cursor = conn.cursor()
        
        # Insert data into the database
        insert_sql = """
        INSERT INTO nba_data (table_name, data) 
        VALUES (%s, %s)
        """
        
        # Prepare data for insertion
        data_to_insert = [(table_name, record) for record in records]
        
        # Use execute_values for better performance
        execute_values(
            cursor, 
            insert_sql, 
            data_to_insert,
            template=None,
            page_size=1000
        )
        
        conn.commit()
        logger.info(f"Successfully loaded {len(records)} records from {csv_file_path}")
        
    except Exception as e:
        logger.error(f"Error loading {csv_file_path}: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()

def load_all_processed_files(conn, processed_data_dir="processed_data"):
    """Load all processed CSV files into the database."""
    processed_files = glob.glob(f"{processed_data_dir}/processed_*.csv")
    
    if not processed_files:
        logger.warning("No processed files found. Run download_dataset.py first.")
        return
    
    logger.info(f"Found {len(processed_files)} processed files to load")
    
    for file_path in processed_files:
        # Extract table name from filename
        table_name = Path(file_path).stem.replace('processed_', '')
        
        try:
            load_csv_to_database(conn, file_path, table_name)
        except Exception as e:
            logger.error(f"Failed to load {file_path}: {e}")
            continue

def create_sample_queries(conn):
    """Create some sample queries to demonstrate the data."""
    cursor = conn.cursor()
    
    sample_queries = [
        """
        -- Get all available tables
        SELECT DISTINCT table_name, COUNT(*) as record_count 
        FROM nba_data 
        GROUP BY table_name 
        ORDER BY record_count DESC;
        """,
        
        """
        -- Example: Find players with high scoring averages
        SELECT data->>'player' as player_name, 
               data->>'pts' as points,
               data->>'season' as season
        FROM nba_data 
        WHERE table_name LIKE '%player%' 
        AND data->>'pts' IS NOT NULL
        AND (data->>'pts')::numeric > 25
        ORDER BY (data->>'pts')::numeric DESC
        LIMIT 10;
        """,
        
        """
        -- Example: Team statistics
        SELECT data->>'team' as team_name,
               COUNT(*) as games_played
        FROM nba_data 
        WHERE data->>'team' IS NOT NULL
        GROUP BY data->>'team'
        ORDER BY games_played DESC
        LIMIT 10;
        """
    ]
    
    logger.info("Sample queries created. You can run these to explore the data:")
    for i, query in enumerate(sample_queries, 1):
        logger.info(f"\nQuery {i}:")
        logger.info(query)

def main():
    """Main function to set up the database and load data."""
    try:
        # Create database connection
        conn = create_connection()
        
        # Create tables
        create_tables(conn)
        
        # Load processed files
        load_all_processed_files(conn)
        
        # Create sample queries
        create_sample_queries(conn)
        
        logger.info("Database setup complete!")
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
