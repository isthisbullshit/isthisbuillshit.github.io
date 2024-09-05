import json

import numpy
from fastapi import FastAPI
from pydantic import BaseModel

from algorithm import load_algorithm_from_directory

app = FastAPI()
algorithm = load_algorithm_from_directory("model")
@app.get("/")
async def root():
    return {"message": "Hello World"}


class Query(BaseModel):
    text: str
@app.post("/")
async def bs_predictor(query: Query):
    bs_score : numpy.ndarray = algorithm.predict([query.text])
    return {"bs_score": bs_score.tolist()}
