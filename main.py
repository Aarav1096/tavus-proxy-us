from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

TAVUS_API_KEY = os.getenv("TAVUS_API_KEY")
REPLICA_ID = os.getenv("REPLICA_ID")

TAVUS_API = "https://api.tavus.io"

@app.post("/videos")
async def create_video(request: Request):
    payload = await request.json()
    payload["replica_id"] = REPLICA_ID
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TAVUS_API}/videos",
            json=payload,
            headers={
                "x-api-key": TAVUS_API_KEY,
                "Content-Type": "application/json",
            },
        )
    return response.json()

@app.get("/videos/{video_id}")
async def get_video(video_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{TAVUS_API}/videos/{video_id}",
            headers={
                "x-api-key": TAVUS_API_KEY
            },
        )
    return response.json()
