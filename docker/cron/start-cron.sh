#!/bin/bash

# Kill any existing cron processes
pkill cron || true

# Create log directory
mkdir -p /var/log

# Create cron job with correct syntax (5 fields + user + command)
echo "*/2 * * * * root docker exec lambda-csv-batch-ctr python /app/processor.py >> /var/log/cron.log 2>&1" > /etc/cron.d/batch-job

# Add empty line at end (required for cron.d files)
echo "" >> /etc/cron.d/batch-job

# Set correct permissions
chmod 0644 /etc/cron.d/batch-job

# Ensure log file exists
touch /var/log/cron.log

# Install the cron job
crontab /etc/cron.d/batch-job

# Start cron in foreground
echo "Starting cron daemon..."
cron -f
