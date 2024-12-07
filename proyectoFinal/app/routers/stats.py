from fastapi import APIRouter
from app.models.loader import load_model

router = APIRouter()
model = load_model("models/modeloRandomForest.pkl")

@router.get("/")
def get_model_stats():
    feature_importances = model.feature_importances_
    feature_names = [
        "Age", "Gender", "Tenure", "Usage_Frequency", "Support_Calls",
        "Payment_Delay", "Subscription_Type", "Contract_Length",
        "Total_Spend", "Last_Interaction"
    ]
    importance_dict = [{"feature": name, "importance": imp} for name, imp in zip(feature_names, feature_importances)]

    return {
        "metrics": {
            "Precision": 0.9982,
            "Recall": 0.9716,
            "F1": 0.9847,
            "Roc_Auc": 0.9864
        },
        "features_importance": sorted(importance_dict, key=lambda x: x["importance"], reverse=True)
    }