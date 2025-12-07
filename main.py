from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TAVUS_API_KEY = os.getenv("TAVUS_API_KEY")
REPLICA_ID = os.getenv("REPLICA_ID")
TAVUS_API = "https://api.tavus.io"


@app.get("/")
def home():
    return {"status": "Proxy active", "has_routes": True}


@app.post("/videos")
async def create_video(request: Request):
    payload = await request.json()
    payload["replica_id"] = REPLICA_ID

    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{TAVUS_API}/videos",
            json=payload,
            headers={
                "x-api-key": TAVUS_API_KEY,
                "Content-Type": "application/json",
            },
            timeout=40,
        )
    return res.json()


@app.get("/videos/{video_id}")
async def get_video(video_id: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{TAVUS_API}/videos/{video_id}",
            headers={"x-api-key": TAVUS_API_KEY},
            timeout=40,
        )
    return res.json()

    
