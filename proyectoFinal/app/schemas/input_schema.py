from pydantic import BaseModel, Field
from typing import Literal

class PredictionInput(BaseModel):
    CustomerID: str = Field(..., description="Identificador único del cliente.")
    Age: int = Field(..., ge=18, le=100, description="Edad del cliente, entre 18 y 100 años.")
    Gender: Literal["Male", "Female"] = Field(..., description="Género del cliente ('Male' o 'Female').")
    Tenure: int = Field(..., ge=1, description="Tiempo en la empresa (meses).")
    Usage_Frequency: int = Field(..., ge=0, description="Frecuencia de uso promedio.")
    Support_Calls: int = Field(..., ge=0, description="Número de llamadas al soporte técnico.")
    Payment_Delay: int = Field(..., ge=0, description="Días de retraso en el pago.")
    Subscription_Type: Literal["Basic", "Standard", "Premium"] = Field(
        ..., description="Tipo de suscripción ('Basic', 'Standard', 'Premium')."
    )
    Contract_Length: Literal["Monthly", "Quarterly", "Annual"] = Field(
        ..., description="Duración del contrato ('Monthly', 'Quarterly', 'Annual')."
    )
    Total_Spend: int = Field(..., ge=0, description="Gasto total del cliente.")
    Last_Interaction: int = Field(..., ge=0, description="Tiempo desde la última interacción (días).")
