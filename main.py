from fastapi import FastAPI, UploadFile, File
import requests
import time
import os

app = FastAPI()

# Yaha apni Meshy API Key daal de
MESHY_API_KEY = "msy_68X0wWn6g8AUmhL0KphYyGoJNa5i7PHJZQWr"
HEADERS = {"Authorization": f"Bearer {MESHY_API_KEY}"}

@app.post("/banau-murti")
async def banau_murti(photo: UploadFile = File(...)):
    # 1. Photo ko Meshy ko bheja
    files = {"image": (photo.filename, await photo.read())}
    data = {"mode": "preview", "art_style": "realistic"}
    
    res = requests.post(
        "https://api.meshy.ai/openapi/v1/image-to-3d",
        headers=HEADERS, files=files, data=data
    ).json()
    
    task_id = res["result"]
    print("Task shuru:", task_id)

    # 2. Wait karo jab tak Meshy bana na de - 2-3 min
    for i in range(60):
        time.sleep(5)
        status = requests.get(
            f"https://api.meshy.ai/openapi/v1/image-to-3d/{task_id}",
            headers=HEADERS
        ).json()
        
        if status["status"] == "SUCCEEDED":
            # 3. Ban gayi! GLB ka link wapas bhejo
            return {
                "status": "ho_gaya",
                "glb_url": status["model_urls"]["glb"],
                "thumbnail": status["thumbnail_url"]
            }
        if status["status"] == "FAILED":
            return {"status": "fail", "reason": status}

    return {"status": "time_lag_gaya"}

@app.get("/")
def home():
    return {"bol": "Backend chal raha hai bhai!"}
