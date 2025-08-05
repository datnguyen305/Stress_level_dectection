@echo off
REM Reset Airflow Environment Script (Windows)

echo 🛑 Stopping all running containers...
docker-compose down -v

echo 🗑️ Removing old volumes and containers...
docker volume prune -f
docker container prune -f

echo 🧹 Cleaning up Airflow database...
docker-compose run --rm airflow-init bash -c "rm -rf /opt/airflow/logs/* && rm -rf /opt/airflow/airflow.db"

echo 🐳 Rebuilding Docker images...
docker-compose build --no-cache

echo 🗄️ Initializing fresh Airflow database...
docker-compose run --rm airflow-init airflow db init

echo 👤 Creating admin user...
docker-compose run --rm airflow-create-user

echo ✅ Reset completed! Starting Airflow...
docker-compose up -d

echo.
echo 🌍 Access Airflow UI at: http://localhost:8080
echo    Username: admin
echo    Password: admin
echo.
echo 📊 To view logs: docker-compose logs -f

pause
