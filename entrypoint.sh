#!/bin/bash
set -ex

echo '=== DEBUGGING CONNECTIVITY ==='
echo "Testing connection to ${DB_HOST}:${DB_PORT}..."

# Wait for PostgreSQL with retries
until pg_isready -h ${DB_HOST} -U ${DB_USER}; do
  echo "Waiting for database..."
  sleep 2
done

# Test database connection
echo 'Testing database connection...'
# Set PGPASSWORD so the psql command can use it
export PGPASSWORD=${DB_PASSWORD}
psql -h ${DB_HOST} -U ${DB_USER} -d ${DB_NAME} -c 'SELECT 1;' || echo 'Database connection failed'
export PGPASSWORD="" # Clear the password from the environment for security


echo '=== STARTING AIRFLOW ==='

# Verify `pip` exists and its location
echo 'Verifying pip installation...'
which pip # This will show if `pip` is in the PATH. It should output the path, or an error if not found.

# Install required providers
echo 'Installing required providers...'
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir "apache-airflow-providers-docker>=3.12.0" "apache-airflow-providers-postgres>=5.0.0"

# Initialize Airflow database (creates airflow tables in the same DB)
echo 'Initializing Airflow database...'
airflow db init

# Create admin user
echo 'Creating admin user...'
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com || echo 'User already exists'

# Start webserver in the background
airflow webserver --port 8080 &

# Start the scheduler in the foreground, which keeps the container running
exec airflow scheduler