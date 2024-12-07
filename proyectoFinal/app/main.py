from fastapi import FastAPI
from app.routers import predictions, health, stats

app = FastAPI(
    title="API de Predicción de Deserción",
    description="Esta API predice la deserción de clientes y proporciona estadísticas del modelo.",
    version="1.0.0",
)

@app.get("/")
def root():
    """
    Endpoint raíz para verificar que la API está activa.
    """
    return {"message": "API de Predicción de Deserción está activa y funcionando correctamente."}

# Registrar rutas con prefijos
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(stats.router, prefix="/api/stats", tags=["Statistics"])