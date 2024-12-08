from fastapi import APIRouter, HTTPException
from app.models.loader import load_model
from app.schemas.input_schema import PredictionInput
from app.services.predictor import make_prediction

router = APIRouter()
model = load_model("models/modeloRandomForest.pkl")

@router.post("/")
def predict(input_data: list[PredictionInput]):
    try:
        results = []
        for data in input_data:
            prediction = make_prediction(model, data)
            results.append({"received_data": data.dict(), **prediction})
        return {"predictions": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durante la predicción: {str(e)}")