FROM python:3.11.12-slim-bullseye
WORKDIR /app
COPY ingestion.py .
RUN pip install --no-cache-dir requests watchdog
RUN mkdir -p /app/data_Crawl
VOLUME /app/data_Crawl
ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
CMD ["python", "ingestion.py"]