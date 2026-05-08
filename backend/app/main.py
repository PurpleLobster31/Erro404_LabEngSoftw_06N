from fastapi import FastAPI
from backend.app.routers import unidades, atendimentos, pacientes
from backend.database.seed import run_seed
 
app = FastAPI(
    title="MedTime API",
    description="API para consulta de tempos de espera em unidades de saúde.",
    version="0.1.0",
)
 
app.include_router(unidades.router)
app.include_router(atendimentos.router)
# app.include_router(pacientes.router)
 
@app.on_event("startup")
async def startup_event():
    """Popula o banco de dados com dados iniciais na inicialização."""
    await run_seed()
 
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": "MedTime API"}
 
 
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}