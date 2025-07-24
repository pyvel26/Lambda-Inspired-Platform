FROM debian:stable-slim

ENV TZ=America/New_York

# Install dependencies
RUN apt-get update && \
    apt-get install -y cron docker.io bash tzdata && \
    apt-get clean

# Create cron job file with correct permissions
COPY start-cron.sh /start-cron.sh
RUN chmod +x /start-cron.sh

# Set working directory (optional but good hygiene)
WORKDIR /

# Start cron service in foreground
CMD ["bash", "/start-cron.sh"]
