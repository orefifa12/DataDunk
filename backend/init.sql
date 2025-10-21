-- Initialize NBA Database
-- This script runs when the PostgreSQL container starts for the first time

-- Create the main NBA data table
CREATE TABLE IF NOT EXISTS nba_data (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_nba_data_table_name ON nba_data(table_name);
CREATE INDEX IF NOT EXISTS idx_nba_data_jsonb ON nba_data USING GIN(data);

-- Create a view for easy data exploration
CREATE OR REPLACE VIEW nba_data_summary AS
SELECT 
    table_name,
    COUNT(*) as record_count,
    MIN(created_at) as first_loaded,
    MAX(created_at) as last_updated
FROM nba_data 
GROUP BY table_name
ORDER BY record_count DESC;

-- Grant permissions to the nba_user
GRANT ALL PRIVILEGES ON DATABASE nba_data TO nba_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nba_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO nba_user;
