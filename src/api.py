from fastapi import FastAPI
from pydantic import BaseModel
from src.predict import load_model, predict
from src.kafka_producer import get_producer

app = FastAPI(title="Bike Sharing Prediction API")
model = load_model()


class BikeFeatures(BaseModel):
    season: int
    holiday: int
    workingday: int
    weather: int
    temp: float
    humidity: float
    windspeed: float
    hour: int
    dayofweek: int
    month: int


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/predict")
def get_prediction(features: BikeFeatures):
    result = predict(model, features.model_dump())
    get_producer().send("predictions", value={"input": features.model_dump(), "result": result})
    return {"predicted_count": result}