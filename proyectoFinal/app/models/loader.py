import joblib
import os

def load_model(model_path: str):
    absolute_path = os.path.join(os.path.dirname(__file__), "..", model_path)
    try:
        return joblib.load(absolute_path)
    except FileNotFoundError:
        raise RuntimeError(f"No se encontró el modelo en la ruta: {model_path}")