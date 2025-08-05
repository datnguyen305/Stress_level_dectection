@echo off
echo 🔧 Fixing Airflow Database Version Issue...

echo 🛑 Step 1: Stop all containers
docker-compose down

echo 🗑️ Step 2: Remove old database volume  
docker volume rm stress_level_dectection_postgres-db-volume 2>nul

echo 🐳 Step 3: Start only PostgreSQL
docker-compose up -d postgres

echo ⏳ Step 4: Wait for PostgreSQL to be ready...
timeout /t 10

echo 🗄️ Step 5: Initialize fresh database
docker-compose run --rm airflow-init airflow db init

echo 👤 Step 6: Create admin user
docker-compose run --rm airflow-create-user

echo 🚀 Step 7: Start all services
docker-compose up -d

echo ✅ Fix completed!
echo.
echo 🌍 Access Airflow at: http://localhost:8080
echo    Username: admin  
echo    Password: admin

pause
