from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    CustomerID: str = Field(..., description="Identificador único del cliente.")
    Age: int = Field(..., ge=18, le=100, description="Edad del cliente, entre 18 y 100 años.")
    Gender: str = Field(..., ge=0, le=1, description="Género codificado (0: Femenino, 1: Masculino).")
    Tenure: int = Field(..., ge=1, description="Tiempo en la empresa (meses).")
    Usage_Frequency: int = Field(..., ge=0, description="Frecuencia de uso promedio.")
    Support_Calls: int = Field(..., ge=0, description="Número de llamadas al soporte técnico.")
    Payment_Delay: int = Field(..., ge=0, description="Días de retraso en el pago.")
    Subscription_Type: str = Field(..., ge=0, le=2, description="Tipo de suscripción codificada.")
    Contract_Length: str = Field(..., ge=0, le=2, description="Duración del contrato codificada.")
    Total_Spend: int = Field(..., ge=0, description="Gasto total del cliente.")
    Last_Interaction: int = Field(..., ge=0, description="Tiempo desde la última interacción (días).")
