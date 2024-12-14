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

        required_features = [
            "Age", "Tenure", "Usage_Frequency", 
            "Support_Calls", "Payment_Delay", 
            "Total_Spend", "Last_Interaction",
            "Contract_Length", "Gender", "Subscription_Type"
        ]

        input_features = {key: input_data[key] for key in required_features}
        input_df = pd.DataFrame([input_features])

        column_mapping = {
            "Last_Interaction": "Last Interaction",
            "Payment_Delay": "Payment Delay",
            "Support_Calls": "Support Calls",
            "Total_Spend": "Total Spend",
            "Usage_Frequency": "Usage Frequency",
            "Contract_Length": "Contract Length",
            "Gender": "Gender",
            "Subscription_Type": "Subscription Type"
        }
        input_df.rename(columns=column_mapping, inplace=True)

        numeric_features = [
            "Age", "Tenure", "Usage_Frequency", 
            "Support Calls", "Payment Delay", 
            "Total Spend", "Last Interaction"
        ]
        normalized_data = normalize_data(input_df[numeric_features])
        normalized_df = pd.DataFrame(normalized_data, columns=numeric_features)

        for col in ["Contract Length", "Gender", "Subscription Type"]:
            normalized_df[col] = input_df[col].values

        prediction = model.predict(normalized_df)[0]
        probability = model.predict_proba(normalized_df)[0].tolist()

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
