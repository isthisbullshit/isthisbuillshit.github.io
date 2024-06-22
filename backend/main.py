from datetime import datetime
from typing import Optional, Annotated
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Cookie, Request, Header
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
    allow_origins=origins,
    allow_credentials=True,
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
async def bullshitAI(bs: Bullshit, request: Request, user_agent: Annotated[str | None, Header()] = None, cookie: Optional[str] = Cookie(None)):
    if cookie is None:
        cookie = str(uuid.uuid4())

    with open(f"data/{datetime.now().timestamp()}{cookie}", 'w') as fp:
        fp.write(f"{str(bs)} \n\n {request.client.host} \n\n {user_agent}")

    response = JSONResponse(content={"message": "Great BS"})
    response.set_cookie(key="session", value=cookie)

    return {"I am good. Thank you!"}

