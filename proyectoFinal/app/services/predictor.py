import numpy as np
import pandas as pd

def make_prediction(model, input_data):
    try:
        required_fields = [
            "Age", "Gender", "Support_Calls", 
            "Payment_Delay", "Subscription_Type", 
            "Total_Spend", "Last_Interaction"
        ]
        missing_fields = [field for field in required_fields if not hasattr(input_data, field)]
        if missing_fields:
            raise ValueError(f"Faltan campos requeridos en input_data: {missing_fields}")

        input_features = pd.DataFrame([{
            "Age": input_data.Age,
            "Gender": input_data.Gender,
            "Support_Calls": input_data.Support_Calls,
            "Payment_Delay": input_data.Payment_Delay,
            "Subscription_Type": input_data.Subscription_Type,
            "Total_Spend": input_data.Total_Spend,
            "Last_Interaction": input_data.Last_Interaction
        }])

        prediction = model.predict(input_features)[0]
        probability = model.predict_proba(input_features)[0].tolist()

        return {
            "prediction": int(prediction),
            "probability": probability,
            "interpretation": "Cliente en riesgo de desertar" if prediction == 1 else "Cliente leal"
        }
    except Exception as e:
        raise RuntimeError(f"Error durante la predicción: {str(e)}")