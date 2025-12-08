from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import socket
import httpx._config as httpx_config


# Force IPv4 + avoid IPv6 issues
httpx_config.DEFAULT_BACKOFF_FACTOR = 0
socket.setdefaulttimeout(30)


app = FastAPI()

# Enable CORS so Flask frontend can call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Tavus credentials
TAVUS_API_KEY = os.getenv("TAVUS_API_KEY")
REPLICA_ID = os.getenv("REPLICA_ID")

TAVUS_API = "https://api.tavus.io"


@app.get("/")
def home():
    return {
        "status": "Proxy active",
        "has_routes": True,
        "api_loaded": bool(TAVUS_API_KEY),
        "replica_loaded": bool(REPLICA_ID),
    }


@app.post("/videos")
async def create_video(request: Request):
    payload = await request.json()
    payload["replica_id"] = REPLICA_ID

    print("\n### CREATE VIDEO PAYLOAD:", payload)

    # Force IPv4 through local_address="0.0.0.0"
    async with httpx.AsyncClient(
        transport=httpx.AsyncHTTPTransport(retries=2, local_address="0.0.0.0")
    ) as client:
        response = await client.post(
            f"{TAVUS_API}/videos",
            json=payload,
            headers={
                "x-api-key": TAVUS_API_KEY,
                "Content-Type": "application/json",
            },
            timeout=60,
        )

    print("### Tavus Response Code:", response.status_code)
    print("### Tavus Response:", response.text)

    try:
        return response.json()
    except:
        return {"error": "Invalid JSON response from Tavus", "raw": response.text}


@app.get("/videos/{video_id}")
async def get_video(video_id: str):

    print(f"\n### POLLING VIDEO ID: {video_id}")

    async with httpx.AsyncClient(
        transport=httpx.AsyncHTTPTransport(retries=2, local_address="0.0.0.0")
    ) as client:
        response = await client.get(
            f"{TAVUS_API}/videos/{video_id}",
            headers={"x-api-key": TAVUS_API_KEY},
            timeout=60,
        )

    print("### Tavus Poll Response Code:", response.status_code)
    print("### Tavus Poll Response:", response.text)

    try:
        return response.json()
    except:
        return {"error": "Invalid JSON response when polling Tavus", "raw": response.text}
