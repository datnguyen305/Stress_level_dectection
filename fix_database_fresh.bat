@echo off
echo ===========================================
echo  KHOI TAO AIRFLOW HOAN TOAN MOI
echo ===========================================

echo.
echo 1. Dung tat ca container va xoa volume...
docker-compose down -v

echo.
echo 2. Tao lai database bang db migrate...
docker-compose run --rm airflow-init airflow db migrate

echo.
echo 3. Tao admin user...
docker-compose run --rm airflow-create-user airflow users create ^
    --username admin ^
    --password admin ^
    --firstname Admin ^
    --lastname User ^
    --role Admin ^
    --email admin@example.com

echo.
echo 4. Khoi dong tat ca dich vu...
docker-compose up -d

echo.
echo ===========================================
echo  HOAN TAT KHOI TAO!
echo  Airflow UI: http://localhost:8080
echo  Username: admin
echo  Password: admin
echo ===========================================
