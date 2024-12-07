from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    Age: float = Field(..., ge=18, le=100, description="Edad del cliente, entre 18 y 100 años.")
    Gender: int = Field(..., ge=0, le=1, description="Género codificado (0: Femenino, 1: Masculino).")
    # Tenure: float = Field(..., ge=1, description="Tiempo en la empresa (meses).")
    # Usage_Frequency: float = Field(..., ge=0, description="Frecuencia de uso promedio.")
    Support_Calls: float = Field(..., ge=0, description="Número de llamadas al soporte técnico.")
    Payment_Delay: float = Field(..., ge=0, description="Días de retraso en el pago.")
    Subscription_Type: int = Field(..., ge=0, le=2, description="Tipo de suscripción codificada.")
    # Contract_Length: int = Field(..., ge=0, le=2, description="Duración del contrato codificada.")
    Total_Spend: float = Field(..., ge=0, description="Gasto total del cliente.")
    Last_Interaction: float = Field(..., ge=0, description="Tiempo desde la última interacción (días).")