from fastapi import FastAPI
import subprocess

app = FastAPI(root_path="/api/crawl")
@app.post("/crawl-now")
def crawl_now():
    result = subprocess.run(["python", "dataCraw.py"], capture_output=True, text=True)
    return {
        "status": "done",
        "stdout": result.stdout[-300:],  # Giới hạn log trả về
        "stderr": result.stderr
    }
