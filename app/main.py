from fastapi import FastAPI
from app.routers import unidades, atendimentos, pacientes
 
app = FastAPI(
    title="MedTime API",
    description="API para consulta de tempos de espera em unidades de saúde.",
    version="0.1.0",
)
 
app.include_router(unidades.router)
app.include_router(atendimentos.router)
app.include_router(pacientes.router)
 
 
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": "MedTime API"}
 
 
@app.get("/ping", tags=["Health"])
def health_check():
    return {"status": "ok"}