# DataDunk NBA Database Setup

This guide will help you set up the NBA database using Docker for the DataDunk project.

## Prerequisites

- Docker and Docker Compose installed on your machine
- Git (to clone the repository)

## Quick Start

1. **Clone the repository** (if not already done):

   ```bash
   git clone <repository-url>
   cd DataDunk
   ```

2. **Start the services**:

   ```bash
   docker-compose up -d
   ```

3. **Wait for data processing** (this may take a few minutes):

   ```bash
   docker-compose logs -f data-processor
   ```

4. **Access the database**:
   - **pgAdmin (Web Interface)**: http://localhost:8080
     - Email: admin@datadunk.com
     - Password: admin123
   - **Direct PostgreSQL**: localhost:5432
     - Database: nba_data
     - User: nba_user
     - Password: nba_password

## Services Overview

### 1. PostgreSQL Database (`db`)

- **Port**: 5432
- **Database**: nba_data
- **User**: nba_user
- **Password**: nba_password

### 2. Data Processor (`data-processor`)

- Downloads NBA dataset from Kaggle
- Processes and loads data into PostgreSQL
- Runs automatically when the database is ready

### 3. pgAdmin (`pgadmin`)

- **Port**: 8080
- **Email**: admin@datadunk.com
- **Password**: admin123
- Web-based PostgreSQL administration tool

## Connecting to the Database

### Using psql (command line)

```bash
docker-compose exec db psql -U nba_user -d nba_data
```

### Using Python

```python
import psycopg2

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='nba_data',
    user='nba_user',
    password='nba_password'
)
```

### Using pgAdmin

1. Open http://localhost:8080
2. Login with admin@datadunk.com / admin123
3. Add new server:
   - Host: db
   - Port: 5432
   - Database: nba_data
   - Username: nba_user
   - Password: nba_password

## Sample Queries

### View all available data tables

```sql
SELECT * FROM nba_data_summary;
```

### Find high-scoring players

```sql
SELECT data->>'player' as player_name,
       data->>'pts' as points,
       data->>'season' as season
FROM nba_data
WHERE table_name LIKE '%player%'
AND data->>'pts' IS NOT NULL
AND (data->>'pts')::numeric > 25
ORDER BY (data->>'pts')::numeric DESC
LIMIT 10;
```

### Team statistics

```sql
SELECT data->>'team' as team_name,
       COUNT(*) as games_played
FROM nba_data
WHERE data->>'team' IS NOT NULL
GROUP BY data->>'team'
ORDER BY games_played DESC
LIMIT 10;
```

## Useful Commands

### View logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs db
docker-compose logs data-processor
```

### Restart services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart db
```

### Stop services

```bash
docker-compose down
```

### Remove everything (including data)

```bash
docker-compose down -v
```

## Troubleshooting

### Database connection issues

1. Check if the database is running: `docker-compose ps`
2. Check database logs: `docker-compose logs db`
3. Ensure the database is healthy: `docker-compose exec db pg_isready -U nba_user -d nba_data`

### Data processing issues

1. Check data processor logs: `docker-compose logs data-processor`
2. Restart data processing: `docker-compose restart data-processor`

### Port conflicts

If ports 5432 or 8080 are already in use, modify the `docker-compose.yml` file:

```yaml
ports:
  - "5433:5432" # Change 5432 to 5433
```

## Data Structure

The NBA data is stored in a flexible JSONB format in the `nba_data` table:

- `id`: Primary key
- `table_name`: Name of the original CSV file
- `data`: JSONB containing all the row data
- `created_at`: Timestamp when the data was loaded

This structure allows for flexible querying of different NBA datasets while maintaining data integrity.

## Team Collaboration

All team members can use the same setup:

1. Pull the latest changes: `git pull`
2. Start the services: `docker-compose up -d`
3. Access the database using the credentials above

The database data persists between restarts, so you don't need to reload the data every time.
