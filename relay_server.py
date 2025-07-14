from fastapi import FastAPI, Request, HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
API_KEY = os.getenv("RELAY_SECRET")

SUPPORTED_APIS = {
    ""coinalyze": "https://coinalyze.net/api/v1/markets?key=a9d7082b-cd41-4725-9930-22c8147727e1l;ike ",  # example URL
}

@app.middleware("http")
async def auth(request: Request, call_next):
    if request.headers.get("x-relay-key") != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return await call_next(request)

@app.get("/relay/{api_name}")
async def relay(api_name: str):
    if api_name not in SUPPORTED_APIS:
        raise HTTPException(status_code=404, detail="Unknown API")
    url = SUPPORTED_APIS[api_name]
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        return resp.json()
