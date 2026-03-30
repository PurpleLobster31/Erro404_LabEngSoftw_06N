from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.unidade import UnidadeResponse
from app import database

router = APIRouter(prefix="/unidades", tags=["Unidades"])


@router.get("/", response_model=List[UnidadeResponse])
def listar_unidades(
    nome: Optional[str] = Query(None, description="Filtrar por nome (UC008 - Pesquisar Hospitais)")
):
    """
    Lista todas as unidades de saúde com tempo médio de espera (UC001).
    Aceita filtro por nome para busca textual (UC008).
    """
    unidades = list(database.unidades_db.values())
    if nome:
        unidades = [u for u in unidades if nome.lower() in u["nome"].lower()]
        if not unidades:
            raise HTTPException(status_code=404, detail="Nenhuma unidade encontrada para o termo pesquisado.")
    return unidades


@router.get("/{unidade_id}", response_model=UnidadeResponse)
def get_unidade(unidade_id: int):
    """Retorna detalhes e tempo médio de espera de uma unidade específica (UC001)."""
    unidade = database.unidades_db.get(unidade_id)
    if not unidade:
        raise HTTPException(status_code=404, detail="Unidade não encontrada.")
    return unidade