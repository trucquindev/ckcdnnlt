FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install requests fastapi uvicorn supervisor

RUN mkdir -p landing_zone

RUN apt-get update && apt-get install -y cron

COPY cronjob /etc/cron.d/fahasa-cron
RUN chmod 0644 /etc/cron.d/fahasa-cron && crontab /etc/cron.d/fahasa-cron

COPY supervisord.conf /etc/supervisord.conf

CMD ["supervisord", "-c", "/etc/supervisord.conf"]
