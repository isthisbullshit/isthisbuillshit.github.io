from datetime import datetime
import os
import time
from urllib.parse import quote

import aiohttp
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from pydantic import BaseModel
import uuid

try:
    from workers import env as workers_env
except ModuleNotFoundError:
    workers_env = None

from auth import router as auth_router

DEFAULT_ALLOWED_ORIGINS = [
    "https://isthisbullsh.it",
    "https://api.isthisbullsh.it",
]
BS_DETECTOR_URL = os.getenv("BS_DETECTOR_URL", "http://localhost:8001/")
EVENTS_BUCKET_NAME = os.getenv("EVENTS_BUCKET_NAME")
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", ",".join(DEFAULT_ALLOWED_ORIGINS)).split(",")
    if origin.strip()
]
GCP_METADATA_TOKEN_URL = (
    "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
)


class _LocalBucket:
    async def put(self, key: str, content: str) -> None:
        return None


class _GcsBucket:
    def __init__(self, bucket_name: str) -> None:
        self.bucket_name = bucket_name
        self._access_token: str | None = None
        self._expires_at = 0.0

    async def put(self, key: str, content: str) -> None:
        access_token = await self._get_access_token()
        upload_url = (
            "https://storage.googleapis.com/upload/storage/v1/b/"
            f"{quote(self.bucket_name, safe='')}/o"
        )
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "text/plain; charset=utf-8",
        }
        params = {
            "uploadType": "media",
            "name": key,
        }
        async with aiohttp.ClientSession() as client:
            async with client.post(upload_url, params=params, data=content.encode("utf-8"), headers=headers) as response:
                response.raise_for_status()

    async def _get_access_token(self) -> str:
        now = time.time()
        if self._access_token is not None and now < self._expires_at - 60:
            return self._access_token

        headers = {"Metadata-Flavor": "Google"}
        async with aiohttp.ClientSession() as client:
            async with client.get(GCP_METADATA_TOKEN_URL, headers=headers) as response:
                response.raise_for_status()
                token_payload = await response.json()

        self._access_token = token_payload["access_token"]
        self._expires_at = now + int(token_payload.get("expires_in", 0))
        return self._access_token


def _build_event_sink():
    if workers_env is not None:
        return workers_env.BULLSHIT_BUCKET
    if EVENTS_BUCKET_NAME:
        return _GcsBucket(EVENTS_BUCKET_NAME)
    return _LocalBucket()


event_sink = _build_event_sink()

class Bullshit(BaseModel):
    text: str

app = FastAPI()
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _client_address(request: Request) -> str:
    forwarded = request.headers.get("cf-connecting-ip") or request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded
    if request.client is not None and request.client.host:
        return request.client.host
    return "unknown"


async def _write_event(key_prefix: str, cookie: str, request: Request) -> None:
    timestamp = datetime.now().timestamp()
    key = f"{key_prefix}{timestamp}-{cookie}.txt"
    user_agent = request.headers.get("user-agent", "unknown")
    client_address = _client_address(request)
    payload = await request.body()
    body_text = payload.decode("utf-8", errors="replace")
    content = f"{body_text}\n\n{client_address}\n\n{user_agent}"
    await event_sink.put(key, content)


@app.get("/")
async def root():
    return {"check the docs for help"}


@app.get("/health")
async def health():
    return {"I am good. Thank you!"}


@app.post("/metrics")
async def metrics(request: Request):
    cookie = request.cookies.get('session')
    if cookie is None:
        cookie = str(uuid.uuid4())

    await _write_event("metrics/", cookie, request)

    response = JSONResponse(content={"message": "Great BS"})
    response.set_cookie(key="session", value=cookie)

    return response



class Query(BaseModel):
    text: str

@app.post("/bs_score")
async def getBSScore(query: Query, request: Request):
    cookie = request.cookies.get('session')
    if cookie is None:
        cookie = str(uuid.uuid4())

    print("getting bs score")

    await _write_event("get_bs_score/", cookie, request)

    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    payload = {
        "text": query.text
    }

    print("wrote logs")

    async with aiohttp.ClientSession() as client:
        async with client.request("POST", BS_DETECTOR_URL, headers=headers, json=payload) as bsRequest:
            print("awaiting response")
            json_response = await bsRequest.json()
            response = JSONResponse(content=json_response)
    response.set_cookie(key="session", value=cookie)

    return response
