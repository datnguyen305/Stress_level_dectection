FROM apache/airflow:2.9.1-python3.11

# Install OS packages with root privileges
USER root
RUN apt-get update && apt-get install -y gcc g++ libpq-dev && apt-get clean

# Copy requirements file
COPY requirements.txt /requirements.txt

# Switch to airflow user before installing pip packages
USER airflow
RUN pip install --no-cache-dir -r /requirements.txt

# Copy source code and DAGs
COPY --chown=airflow:root ./src /opt/airflow/src
COPY --chown=airflow:root ./dags /opt/airflow/dags
COPY --chown=airflow:root ./data /opt/airflow/data

# Copy environment file if it exists
COPY --chown=airflow:root .env* /opt/airflow/

# Create necessary directories
USER root
RUN mkdir -p /opt/airflow/logs && chown -R airflow:root /opt/airflow/logs
RUN mkdir -p /opt/airflow/data && chown -R airflow:root /opt/airflow/data

USER airflow

