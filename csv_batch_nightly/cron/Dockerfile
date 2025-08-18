FROM debian:stable-slim

ENV TZ=America/New_York

RUN apt-get update && \
    apt-get install -y cron csv_batch_nightly.io bash tzdata && \
    apt-get clean

# Copy the cron startup script
COPY docker/cron/start-cron.sh /start-cron.sh
RUN chmod +x /start-cron.sh

CMD ["bash", "/start-cron.sh"]