from fastapi import FastAPI
import requests

app = FastAPI()

@app.post("/crawl-now")
def crawl_now():
    res = requests.post("http://data_crawl:8001/crawl-now")
    return res.json()

@app.post("/ingest")
def ingest():
    res = requests.post("http://data_ingestion:8002/ingest")
    return res.json()

@app.get("/products")
def get_products():
    res = requests.get("http://mysql_apifahasa:8002/products")
    return res.json()
