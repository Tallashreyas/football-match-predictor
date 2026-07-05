from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import sys
import os

# Add src folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from predict import predict_match

app = FastAPI(
    title="Football Match Predictor API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MatchRequest(BaseModel):
    home_team: str
    away_team: str


@app.get("/")
def root():
    return {
        "message": "Football Match Predictor API is running!"
    }


@app.get("/teams")
def get_teams():

    from predict import teams

    return {
        "teams": teams
    }


@app.post("/predict")
def predict(data: MatchRequest):

    try:

        result = predict_match(
            data.home_team,
            data.away_team
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )