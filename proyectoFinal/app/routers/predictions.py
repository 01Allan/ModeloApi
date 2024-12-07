from fastapi import APIRouter, HTTPException
from app.models.loader import load_model
from app.schemas.input_schema import PredictionInput
from app.services.predictor import make_prediction

router = APIRouter()
model = load_model("proyectoFinal/app/models/modelo_random_forest.pkl")

@router.post("/")
def predict(input_data: PredictionInput):
    try:
        result = make_prediction(model, input_data)
        return {"received_data": input_data.dict(), **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durante la predicción: {str(e)}")