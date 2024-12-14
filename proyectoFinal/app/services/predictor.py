import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from app.services.database import save_prediction_to_db
from app.services.logger import logger

def normalize_data(data):
    """
    Normalización de datos: Logarítmica seguida de Z-Score.
    """
    log_transformed = np.log1p(data)
    scaler = StandardScaler()
    normalized = scaler.fit_transform(log_transformed) 
    return normalized

def make_prediction(model, input_data):
    try:
 
        if not isinstance(input_data, dict):
            input_data = input_data.dict()

        column_mapping = {
            "Last_Interaction": "Last Interaction",
            "Payment_Delay": "Payment Delay",
            "Support_Calls": "Support Calls",
            "Total_Spend": "Total Spend",
            "Usage_Frequency": "Usage Frequency",
            "Contract_Length": "Contract Length",
            "Gender": "Gender",
            "Subscription_Type": "Subscription Type",
            "Tenure": "Tenure",
            "Age": "Age"
        }

        input_features = {key: input_data[key] for key in column_mapping if key in input_data}
        input_df = pd.DataFrame([input_features])

        input_df.rename(columns=column_mapping, inplace=True)

        required_features = list(model.feature_names_in_)

        input_df = input_df[required_features]

        numeric_features = [
            "Age", "Tenure", "Usage Frequency", 
            "Support Calls", "Payment Delay", 
            "Total Spend", "Last Interaction"
        ]
        if all(feature in input_df.columns for feature in numeric_features):
            normalized_data = normalize_data(input_df[numeric_features])
            input_df[numeric_features] = normalized_data

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0].tolist()

        db_data = {
            **input_data, 
            "Churn": int(prediction), 
            "Probability": probability[prediction] 
        }

        save_prediction_to_db(db_data)
        logger.info(f"Predicción realizada con éxito para CustomerID {input_data.get('CustomerID')}")

        return {
            "prediction": int(prediction),
            "probability": probability,
            "interpretation": "Cliente en riesgo de desertar" if prediction == 1 else "Cliente leal"
        }

    except Exception as e:
        logger.error(f"Error durante la predicción para CustomerID {input_data.get('CustomerID', 'desconocido')}: {str(e)}")
        raise RuntimeError(f"Error durante la predicción: {str(e)}")
