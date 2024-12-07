import joblib

def load_model(model_path: str):
    try:
        return joblib.load(model_path)
    except FileNotFoundError:
        raise RuntimeError(f"No se encontró el modelo en la ruta: {model_path}")