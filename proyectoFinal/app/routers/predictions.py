from fastapi import APIRouter, HTTPException
from app.models.loader import load_model
from app.services.logger import logger
from app.services.database import save_data_to_db
from app.schemas.input_schema import PredictionInput
from app.services.predictor import process_and_predict

router = APIRouter()
model = load_model("models/modeloDecisionTree.pkl")

# @router.post("/")
# async def predict(input_data: list[PredictionInput]):
#     try:
#         data_as_dicts = [item.dict() for item in input_data]

#         logger.info("Guardando datos recibidos en la base de datos...")
#         save_data_to_db(data_as_dicts)

#         logger.info("Procesando predicciones...")
#         predictions = process_and_predict(model)

#         return {
#             "status": "success",
#             "data_sent": data_as_dicts, 
#             "predictions": predictions 
#         }

#     except Exception as e:
#         logger.error(f"Error general durante la predicción: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Error durante la predicción: {str(e)}")

# SIN BASES
@router.post("/")
async def predict(input_data: list[PredictionInput]):
    try:
        # Procesar las predicciones directamente
        logger.info("Procesando predicciones...")
        predictions = process_and_predict(model, input_data)

        # Retornar los datos enviados y las predicciones
        return {"status": "success", "results": predictions}

    except Exception as e:
        logger.error(f"Error general durante la predicción: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error durante la predicción: {str(e)}")