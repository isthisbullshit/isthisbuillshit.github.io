from datetime import datetime

import aiohttp
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from pydantic import BaseModel
import uuid
from workers import env

from auth import router as auth_router

class Bullshit(BaseModel):
    text: str

app = FastAPI()
app.include_router(auth_router)

origins = [
    "https://isthisbullsh.it",
    "https://api.isthisbullsh.it",
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
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
    await env.BULLSHIT_BUCKET.put(key, content)


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
        async with client.request("POST", "http://localhost:8001/", headers=headers, json=payload) as bsRequest:
            print("awaiting response")
            json_response = await bsRequest.json()
            response = JSONResponse(content=json_response)
    response.set_cookie(key="session", value=cookie)

    return response
