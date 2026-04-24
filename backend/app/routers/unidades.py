from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from geoalchemy2.types import Geography

from backend.app.database import get_db
from backend.app.models import Unidade

router = APIRouter(prefix="/unidades", tags=["Unidades"])

@router.get("/")
async def listar_unidades(
    lat: float = Query(None, description="Latitude da posição atual"),
    lon: float = Query(None, description="Longitude da posição atual"),
    raio_km: float = Query(10.0, description="Raio de busca em quilómetros"),
    db: AsyncSession = Depends(get_db)
):
    # Em vez de apenas select(Unidade), selecionamos explicitamente as colunas 
    # normais e extraímos X e Y da coluna espacial.
    # O label() dá um nome ao resultado para ser acedido no dicionário depois.
    # Removido o cast para Geography dentro de ST_X e ST_Y
    query = select(
        Unidade.id,
        Unidade.nome,
        Unidade.endereco,
        Unidade.tempo_medio_minutos,
        func.ST_Y(Unidade.localizacao).label('latitude'),
        func.ST_X(Unidade.localizacao).label('longitude')
    )

    if lat is not None and lon is not None:
        ponto_utilizador = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
        
        # Mantemos o cast aqui para garantir cálculos em metros
        unidade_geog = func.cast(Unidade.localizacao, Geography)
        utilizador_geog = func.cast(ponto_utilizador, Geography)

        distancia = func.ST_Distance(unidade_geog, utilizador_geog)

        query = query.filter(func.ST_DWithin(unidade_geog, utilizador_geog, raio_km * 1000))
        query = query.add_columns(distancia.label('distancia_metros'))
        query = query.order_by(distancia)

    # Quando usamos select com colunas específicas, o resultado é iterável por linha,
    # não mais objetos SQLAlchemy inteiros (scalars).
    result = await db.execute(query)
    
    # Mapear os resultados linha a linha para uma lista de dicionários para
    # que o FastAPI consiga transformar em JSON perfeitamente.
    unidades_formatadas = []
    for row in result.mappings().all():
        unidades_formatadas.append(dict(row))

    return unidades_formatadas


@router.get("/{id}")
async def obter_unidade(id: int, db: AsyncSession = Depends(get_db)):
    """Get a single unit by ID"""
    query = select(
        Unidade.id,
        Unidade.nome,
        Unidade.endereco,
        Unidade.tempo_medio_minutos,
        func.ST_Y(Unidade.localizacao).label('latitude'),
        func.ST_X(Unidade.localizacao).label('longitude')
    ).where(Unidade.id == id)
    
    result = await db.execute(query)
    row = result.mappings().first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")
    
    return dict(row)
