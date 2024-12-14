import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from app.services.database import save_prediction_to_db

def normalize_data(input_data):
    """
    Normalización de datos: Logarítmica seguida de Z-Score.
    """
    log_transformed = np.log1p(input_data)
    scaler = StandardScaler()
    normalized = scaler.fit_transform(log_transformed)
    return normalized

def make_prediction(model, input_data):
    try:
        if not isinstance(input_data, dict):
            input_data = input_data.dict()

        numeric_features = [
            "Age", "Tenure", "Usage_Frequency", 
            "Support_Calls", "Payment_Delay", 
            "Total_Spend", "Last_Interaction"
        ]
        numeric_data = {key: input_data[key] for key in numeric_features}

        original_df = pd.DataFrame([numeric_data])

        normalized_data = normalize_data(original_df)

        normalized_df = pd.DataFrame(normalized_data, columns=numeric_features)

        prediction = model.predict(normalized_df)[0]
        probability = model.predict_proba(normalized_df)[0].tolist()

        db_data = {
            "CustomerID": input_data["CustomerID"],
            **numeric_data, 
            "Churn": int(prediction),
            "Probability": probability[prediction]
        }
        save_prediction_to_db(db_data)

        return {
            "prediction": int(prediction),
            "probability": probability,
            "interpretation": "Cliente en riesgo de desertar" if prediction == 1 else "Cliente leal"
        }
    except Exception as e:
        raise RuntimeError(f"Error durante la predicción: {str(e)}")