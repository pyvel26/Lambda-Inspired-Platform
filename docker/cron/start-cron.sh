#!/bin/bash

# Define cron job content (note: no asterisk escape needed in shell script)
echo "* * * * * root docker exec realtime-csv-processor-ctr python /app/processor.py >> /var/log/cron.log 2>&1" > /etc/cron.d/batch-job

# Set permissions
chmod 0644 /etc/cron.d/batch-job

# Apply the cron job
crontab /etc/cron.d/batch-job

# Make sure log file exists
touch /var/log/cron.log

# Start cron in foreground
cron -f
