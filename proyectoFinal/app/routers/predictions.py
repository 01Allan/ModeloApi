from fastapi import APIRouter, HTTPException
from app.models.loader import load_model
from app.schemas.input_schema import PredictionInput
from app.services.predictor import make_prediction
from app.services.logger import logger  

router = APIRouter()
model = load_model("models/modeloDecisionTree.pkl")

@router.post("/")
def predict(input_data: list[PredictionInput]):
    """
    Endpoint para realizar predicciones.
    """
    try:
        logger.info("Datos recibidos para predicción: %s", input_data)
        results = []

        for data in input_data:
            try:
                prediction = make_prediction(model, data)
                results.append({
                    "data_recibida": data.dict(),
                    "Prediccion": prediction
                })
                logger.info("Predicción realizada para CustomerID: %s", data.CustomerID)
            except Exception as e:
                logger.error("Error al procesar CustomerID %s: %s", data.CustomerID, str(e))
                raise HTTPException(status_code=500, detail=f"Error en la predicción para CustomerID {data.CustomerID}: {str(e)}")

        logger.info("Predicciones completadas para el lote enviado.")
        return {"predictions": results}

    except Exception as e:
        logger.error("Error general durante la predicción: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Error durante la predicción: {str(e)}")
