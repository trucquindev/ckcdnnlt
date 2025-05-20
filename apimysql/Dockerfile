FROM python:3.11.12-slim-bullseye
COPY . ./apifahasa
RUN pip install fastapi mysql-connector-python uvicorn pandas pydantic
WORKDIR ./apifahasa
CMD ["uvicorn", "fahasaAPI:app", "--host", "0.0.0.0", "--port", "8002"]