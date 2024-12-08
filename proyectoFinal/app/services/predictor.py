import numpy as np

def make_prediction(model, input_data):
    try:
        # Validar atributos en input_data
        required_fields = [
            "Age", "Gender", "Support_Calls", 
            "Payment_Delay", "Subscription_Type", 
            "Total_Spend", "Last_Interaction"
        ]
        missing_fields = [field for field in required_fields if not hasattr(input_data, field)]
        if missing_fields:
            raise ValueError(f"Faltan campos requeridos en input_data: {missing_fields}")

        # Crear las características de entrada
        input_features = np.array([[
            input_data.Age, input_data.Gender, input_data.Tenure,
            input_data.Usage_Frequency, input_data.Support_Calls,
            input_data.Payment_Delay, input_data.Subscription_Type,
            input_data.Contract_Length, input_data.Total_Spend,
            input_data.Last_Interaction
        ]])

        # Generar predicción
        prediction = model.predict(input_features)[0]
        probability = model.predict_proba(input_features)[0].tolist()

        # Formar la respuesta
        return {
            "prediction": int(prediction),
            "probability": probability,
            "interpretation": "Cliente en riesgo de desertar" if prediction == 1 else "Cliente leal"
        }
    except Exception as e:
        raise RuntimeError(f"Error durante la predicción: {str(e)}")