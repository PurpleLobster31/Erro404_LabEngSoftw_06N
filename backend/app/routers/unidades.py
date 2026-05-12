from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_
from geoalchemy2.types import Geography

from backend.app.schemas.unidade import UnidadeResponse
from backend.database.database import get_db
from backend.database.models import Unidade, Atendimento

router = APIRouter(prefix="/unidades", tags=["Unidades"])

@router.get("/")
async def listar_unidades(
    lat: float = Query(None, description="Latitude da posição atual"),
    lon: float = Query(None, description="Longitude da posição atual"),
    raio_km: float = Query(10.0, description="Raio de busca em quilômetros"),
    db: AsyncSession = Depends(get_db)
):
    # CTE 1: Últimos 5 tempos de triagem por unidade
    # Duração em minutos extraída em formato epoch (segundos) dividido por 60
    tempo_triagem_expr = (func.extract('epoch', Atendimento.horario_triagem - Atendimento.horario_chegada) / 60).label('tempo_triagem')
    rn_triagem = func.row_number().over(
        partition_by=Atendimento.unidade_id,
        order_by=Atendimento.horario_triagem.desc()
    ).label('rn')

    cte_triagem_raw = select(
        Atendimento.unidade_id,
        tempo_triagem_expr,
        rn_triagem
    ).where(
        and_(Atendimento.horario_triagem.is_not(None), Atendimento.horario_chegada.is_not(None))
    ).cte('cte_triagem_raw')

    cte_triagem_agg = select(
        cte_triagem_raw.c.unidade_id,
        func.avg(cte_triagem_raw.c.tempo_triagem).label('tempo_medio_triagem')
    ).where(cte_triagem_raw.c.rn <= 5).group_by(cte_triagem_raw.c.unidade_id).cte('cte_triagem_agg')

    # CTE 2: Últimos 5 tempos de atendimento por unidade
    tempo_atend_expr = (func.extract('epoch', Atendimento.horario_atendimento - Atendimento.horario_triagem) / 60).label('tempo_atendimento')
    rn_atend = func.row_number().over(
        partition_by=Atendimento.unidade_id,
        order_by=Atendimento.horario_atendimento.desc()
    ).label('rn')

    cte_atend_raw = select(
        Atendimento.unidade_id,
        tempo_atend_expr,
        rn_atend
    ).where(
        and_(Atendimento.horario_atendimento.is_not(None), Atendimento.horario_triagem.is_not(None))
    ).cte('cte_atend_raw')

    cte_atend_agg = select(
        cte_atend_raw.c.unidade_id,
        func.avg(cte_atend_raw.c.tempo_atendimento).label('tempo_medio_atendimento')
    ).where(cte_atend_raw.c.rn <= 5).group_by(cte_atend_raw.c.unidade_id).cte('cte_atend_agg')

    # Tratamento de valores nulos (COALESCE) para garantir que somas parciais funcionem
    col_triagem = func.coalesce(cte_triagem_agg.c.tempo_medio_triagem, 0).label('tempo_medio_triagem')
    col_atendimento = func.coalesce(cte_atend_agg.c.tempo_medio_atendimento, 0).label('tempo_medio_atendimento')
    col_total = (func.coalesce(cte_triagem_agg.c.tempo_medio_triagem, 0) + func.coalesce(cte_atend_agg.c.tempo_medio_atendimento, 0)).label('tempo_medio_total')

    query = select(
        Unidade.id,
        Unidade.nome,
        Unidade.endereco,
        col_triagem,
        col_atendimento,
        col_total,
        func.ST_Y(Unidade.localizacao).label('latitude'),
        func.ST_X(Unidade.localizacao).label('longitude')
    )

    # Junção das métricas com a tabela de Unidades
    query = query.outerjoin(cte_triagem_agg, Unidade.id == cte_triagem_agg.c.unidade_id)
    query = query.outerjoin(cte_atend_agg, Unidade.id == cte_atend_agg.c.unidade_id)

    if lat is not None and lon is not None:
        ponto_utilizador = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
        unidade_geog = func.cast(Unidade.localizacao, Geography)
        utilizador_geog = func.cast(ponto_utilizador, Geography)
        distancia = func.ST_Distance(unidade_geog, utilizador_geog)
        
        query = query.filter(func.ST_DWithin(unidade_geog, utilizador_geog, raio_km * 1000))
        query = query.add_columns(distancia.label('distancia_metros'))
        query = query.order_by(distancia)

    result = await db.execute(query)

    unidades_formatadas = []
    for row in result.mappings().all():
        unidades_formatadas.append(dict(row))

    return unidades_formatadas


@router.get("/{id}", response_model=UnidadeResponse)
async def obter_unidade(id: int, db: AsyncSession = Depends(get_db)):
    """
    Busca uma unidade pelo ID com cálculo dinâmico de tempos médios 
    (baseado nos últimos 5 atendimentos) e metadados completos.
    """

    # CTE 1: Últimos 5 tempos de triagem por unidade
    tempo_triagem_expr = (func.extract('epoch', Atendimento.horario_triagem - Atendimento.horario_chegada) / 60).label('tempo_triagem')
    rn_triagem = func.row_number().over(
        partition_by=Atendimento.unidade_id,
        order_by=Atendimento.horario_triagem.desc()
    ).label('rn')

    cte_triagem_raw = select(
        Atendimento.unidade_id,
        tempo_triagem_expr,
        rn_triagem
    ).where(
        and_(Atendimento.horario_triagem.is_not(None), Atendimento.horario_chegada.is_not(None))
    ).cte('cte_triagem_raw')

    cte_triagem_agg = select(
        cte_triagem_raw.c.unidade_id,
        func.avg(cte_triagem_raw.c.tempo_triagem).label('tempo_medio_triagem')
    ).where(cte_triagem_raw.c.rn <= 5).group_by(cte_triagem_raw.c.unidade_id).cte('cte_triagem_agg')

    # CTE 2: Últimos 5 tempos de atendimento por unidade
    tempo_atend_expr = (func.extract('epoch', Atendimento.horario_atendimento - Atendimento.horario_triagem) / 60).label('tempo_atendimento')
    rn_atend = func.row_number().over(
        partition_by=Atendimento.unidade_id,
        order_by=Atendimento.horario_atendimento.desc()
    ).label('rn')

    cte_atend_raw = select(
        Atendimento.unidade_id,
        tempo_atend_expr,
        rn_atend
    ).where(
        and_(Atendimento.horario_atendimento.is_not(None), Atendimento.horario_triagem.is_not(None))
    ).cte('cte_atend_raw')

    cte_atend_agg = select(
        cte_atend_raw.c.unidade_id,
        func.avg(cte_atend_raw.c.tempo_atendimento).label('tempo_medio_atendimento')
    ).where(cte_atend_raw.c.rn <= 5).group_by(cte_atend_raw.c.unidade_id).cte('cte_atend_agg')

    # Expressão para o tempo total (Soma das médias)
    col_total = (
        func.coalesce(cte_triagem_agg.c.tempo_medio_triagem, 0) + 
        func.coalesce(cte_atend_agg.c.tempo_medio_atendimento, 0)
    ).label('tempo_medio_minutos')

    # Query Principal com todos os campos do modelo atualizado
    query = select(
        Unidade.id,
        Unidade.nome,
        Unidade.tipo,
        Unidade.endereco,
        Unidade.numero,
        Unidade.complemento,
        Unidade.cep,
        Unidade.cidade,
        Unidade.estado,
        Unidade.telefone1,
        Unidade.telefone2,
        Unidade.descricao,
        Unidade.horario_funcionamento,
        Unidade.imagem_url,
        col_total,
        func.ST_Y(Unidade.localizacao).label('latitude'),
        func.ST_X(Unidade.localizacao).label('longitude')
    ).where(Unidade.id == id)

    # Joins com as agregações
    query = query.outerjoin(cte_triagem_agg, Unidade.id == cte_triagem_agg.c.unidade_id)
    query = query.outerjoin(cte_atend_agg, Unidade.id == cte_atend_agg.c.unidade_id)

    result = await db.execute(query)
    row = result.mappings().first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")
    
    return row
