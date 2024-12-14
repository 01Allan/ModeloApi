from fastapi import APIRouter, HTTPException
from app.models.loader import load_model
from app.schemas.input_schema import PredictionInput
from app.services.predictor import make_prediction
from app.services.logger import logger

router = APIRouter()
model = load_model("models/modeloDecisionTree.pkl")

@router.post("/")
def predict(input_data: list[PredictionInput]):
    try:
        logger.info("Datos recibidos para predicción: %s", input_data)
        results = []
        for data in input_data:
            prediction = make_prediction(model, data)
            results.append({
                "data_recibida": data.dict(),
                "Prediccion": prediction
            })
        logger.info("Predicciones realizadas exitosamente.")
        return {"predictions": results}
    except Exception as e:
        logger.error(f"Error durante la predicción: {e}")
        raise HTTPException(status_code=500, detail=f"Error durante la predicción: {str(e)}")
