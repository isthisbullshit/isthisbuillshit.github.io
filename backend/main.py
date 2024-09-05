from datetime import datetime

import aiohttp
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from pydantic import BaseModel
import uuid
from pathlib import Path

Path("data").mkdir(parents=True, exist_ok=True)

class Bullshit(BaseModel):
    text: str

app = FastAPI()

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

    with open(f"data/{datetime.now().timestamp()}{cookie}", 'w') as fp:
        fp.write(f"{await request.body()} \n\n {request.client.host} \n\n {request.headers['User-Agent']} \n\n {request.headers['x-forwarded-for']}")

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

    with open(f"data/get_bs_score-{datetime.now().timestamp()}{cookie}", 'w') as fp:
        fp.write(f"{await request.body()} \n\n {request.client.host} \n\n {request.headers['User-Agent']} ")

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

