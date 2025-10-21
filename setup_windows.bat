@echo off
echo 🏀 DataDunk NBA Database - Windows Setup
echo ========================================

echo 🔍 Checking Docker...
docker --version
if %errorlevel% neq 0 (
    echo ❌ Docker not found. Please install Docker Desktop
    pause
    exit /b 1
)

echo ✅ Docker found

echo.
echo 🗄️ Starting PostgreSQL database...
docker-compose up -d db

echo ⏳ Waiting for database to initialize...
timeout /t 10 /nobreak > nul

echo.
echo 🐍 Setting up Python environment...
python -m venv venv
call venv\Scripts\activate
pip install psycopg2-binary

echo.
echo 📊 Loading sample data...
python setup_for_team.py

echo.
echo ✅ Setup complete! You can now:
echo   1. Run: python query_players.py
echo   2. Or connect directly to the database
echo.
echo Database connection:
echo   Host: localhost, Port: 5432
echo   Database: nba_data, User: nba_user, Password: nba_password

pause
