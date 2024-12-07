import numpy as np

def make_prediction(model, input_data):
    input_features = np.array([[
        input_data.Age, input_data.Gender, input_data.Tenure,
        input_data.Usage_Frequency, input_data.Support_Calls,
        input_data.Payment_Delay, input_data.Subscription_Type,
        input_data.Contract_Length, input_data.Total_Spend,
        input_data.Last_Interaction
    ]])
    prediction = model.predict(input_features)[0]
    probability = model.predict_proba(input_features)[0].tolist()

    return {
        "prediction": int(prediction),
        "probability": probability,
        "interpretation": "Cliente en riesgo de desertar" if prediction == 1 else "Cliente leal"
    }