import numpy as np
import pandas as pd

def make_prediction(model, input_data):
    try:
        if not isinstance(input_data, dict):
            input_data = input_data.dict()

        required_fields = [
            "Age", "Gender", "Support_Calls", 
            "Payment_Delay", "Subscription_Type", 
            "Total_Spend", "Last_Interaction"
        ]
        missing_fields = [field for field in required_fields if field not in input_data]
        if missing_fields:
            raise ValueError(f"Faltan campos requeridos en input_data: {missing_fields}")

        input_features = pd.DataFrame([[
            input_data["Age"],
            input_data["Gender"],
            input_data["Support_Calls"],
            input_data["Payment_Delay"],
            input_data["Subscription_Type"],
            input_data["Total_Spend"],
            input_data["Last_Interaction"]
        ]], columns=[
            "Age", "Gender", "Support_Calls", 
            "Payment_Delay", "Subscription_Type", 
            "Total_Spend", "Last_Interaction"
        ])

        print("Características de entrada para el modelo:", input_features)

        try:
            prediction = model.predict(input_features)[0]
            probability = model.predict_proba(input_features)[0].tolist()
        except Exception as e:
            raise RuntimeError(f"Error en el modelo: {e}")

        return {
            "prediction": int(prediction),
            "probability": probability,
            "interpretation": "Cliente en riesgo de desertar" if prediction == 1 else "Cliente leal"
        }
    except Exception as e:
        raise RuntimeError(f"Error durante la predicción: {str(e)}")