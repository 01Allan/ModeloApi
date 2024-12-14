import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelBinarizer, LabelEncoder
from app.services.database import (
    fetch_data_from_db,
    save_predictions_to_db
)
from app.services.logger import logger

# def normalize_data(data):
#     """
#     Normalización de datos: Logarítmica seguida de Z-Score.
#     """
#     log_transformed = np.log1p(data)
#     scaler = StandardScaler()
#     normalized = scaler.fit_transform(log_transformed)
#     return normalized

# def process_and_predict(model):
#     try:
#         logger.info("Recuperando datos desde la base de datos para predicción...")
#         data_from_db = fetch_data_from_db()

#         predictions = []
#         for record in data_from_db:
#             try:
#                 column_mapping = {
#                     "Last_Interaction": "Last Interaction",
#                     "Payment_Delay": "Payment Delay",
#                     "Support_Calls": "Support Calls",
#                     "Total_Spend": "Total Spend",
#                     "Usage_Frequency": "Usage Frequency",
#                     "Contract_Length": "Contract Length",
#                     "Gender": "Gender",
#                     "Subscription_Type": "Subscription Type",
#                     "Tenure": "Tenure",
#                     "Age": "Age"
#                 }

#                 input_features = {key: record[key] for key in column_mapping if key in record}
#                 input_df = pd.DataFrame([input_features])

#                 input_df.rename(columns=column_mapping, inplace=True)

#                 required_features = list(model.feature_names_in_)
#                 input_df = input_df[required_features]

#                 numeric_features = [
#                     "Age", "Tenure", "Usage Frequency",
#                     "Support Calls", "Payment Delay",
#                     "Total Spend", "Last Interaction"
#                 ]
#                 if all(feature in input_df.columns for feature in numeric_features):
#                     normalized_data = normalize_data(input_df[numeric_features])
#                     input_df[numeric_features] = normalized_data

#                 prediction = model.predict(input_df)[0]
#                 probability = model.predict_proba(input_df)[0].tolist()

#                 prediction_data = {
#                     "CustomerID": record["CustomerID"],
#                     "Churn": int(prediction),
#                     # "Probability": probability[prediction]
#                 }
#                 save_predictions_to_db([prediction_data])

#                 predictions.append({
#                     "CustomerID": record["CustomerID"],
#                     "prediction": prediction,
#                     # "probability": probability,
#                     "interpretation": "Cliente en riesgo de desertar" if prediction == 1 else "Cliente leal",
#                     "data_sent": record 
#                 })
#             except Exception as e:
#                 logger.error(f"Error en la predicción para CustomerID {record.get('CustomerID', 'desconocido')}: {str(e)}")
#                 continue

#         return predictions

#     except Exception as e:
#         logger.error(f"Error general en el procesamiento de predicciones: {str(e)}")
#         raise RuntimeError(f"Error durante el procesamiento de predicciones: {str(e)}")

def normalize_data(data):
    """
    Normalización de datos: Logarítmica seguida de Z-Score.
    """
    log_transformed = np.log1p(data)
    scaler = StandardScaler()
    normalized = scaler.fit_transform(log_transformed)
    return normalized

def process_and_predict(model, input_data):
    predictions = []
    try:
        # Definir los mapeos
        gender_mapping = {"Male": 1, "Female": 0}
        subscription_mapping = {"Basic": 0, "Standard": 1, "Premium": 2}
        contract_mapping = {"Monthly": 0, "Quarterly": 1, "Annual": 2}

        for record in input_data:
            try:
                record_dict = record.dict()
                record_dict["Gender"] = gender_mapping[record_dict["Gender"]]
                record_dict["Subscription_Type"] = subscription_mapping[record_dict["Subscription_Type"]]
                record_dict["Contract_Length"] = contract_mapping[record_dict["Contract_Length"]]

                input_df = pd.DataFrame([record_dict])

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
                    "Age": "Age",
                }
                input_df.rename(columns=column_mapping, inplace=True)

                required_features = list(model.feature_names_in_)
                input_df = input_df[required_features]

                numeric_features = [
                    "Age", "Tenure", "Usage Frequency", "Support Calls",
                    "Payment Delay", "Total Spend", "Last Interaction"
                ]
                if all(feature in input_df.columns for feature in numeric_features):
                    input_df[numeric_features] = normalize_data(input_df[numeric_features])

                prediction = model.predict(input_df)[0]

                predictions.append({
                    "CustomerID": record_dict["CustomerID"],
                    "prediction": int(prediction),
                    "interpretation": "Cliente en riesgo de desertar" if prediction == 1 else "Cliente leal",
                    "data_sent": record_dict
                })
            except Exception as e:
                logger.error(f"Error en la predicción para CustomerID {record.CustomerID}: {str(e)}")
                continue

        return predictions
    except Exception as e:
        logger.error(f"Error general en el procesamiento de predicciones: {str(e)}")
        raise RuntimeError(f"Error durante el procesamiento de predicciones: {str(e)}")