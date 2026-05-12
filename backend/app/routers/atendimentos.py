from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, desc

from geoalchemy2.types import Geography

from backend.database.database import get_db
from backend.database.models import Atendimento, Paciente, Unidade
from backend.app.schemas.atendimento import (
    AtendimentoCreate,
    AtendimentoAvancar,
    AtendimentoResponse,
    StatusAtendimento,
    AtendimentoGet,
    AtendimentoStatusResponse
)


# Constante de distância em metros para validação de proximidade
RAIO_PERMITIDO_METROS = 100.0

router = APIRouter(prefix="/atendimentos", tags=["Atendimentos"])



@router.get("/ativo", response_model=AtendimentoStatusResponse)
async def buscar_atendimento_ativo(
    payload: AtendimentoGet = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Busca se existe um atendimento em aberto para o paciente em uma unidade nas últimas 24 horas.
    Retorna o estado atualizado para controle de interface (botões).
    """
    limite_tempo = datetime.now() - timedelta(hours=24)

    query = select(Atendimento).where(
        Atendimento.paciente_id == payload.paciente_id,
        Atendimento.unidade_id == payload.unidade_id,
        Atendimento.status == StatusAtendimento.em_aberto,
        Atendimento.horario_chegada >= limite_tempo
    )
    
    result = await db.execute(query)
    atendimento: Atendimento | None = result.scalar_one_or_none()

    # Se não houver atendimento, o estado inicial é o registro de entrada
    if atendimento is None:
        return AtendimentoStatusResponse(
            ativo=False,
            label_botao="Registrar Entrada"
        )

    # Deduz o rótulo do botão com base nos horários já preenchidos
    if atendimento.horario_triagem is None:
        label = "Registrar Triagem"
    else:
        label = "Registrar Atendimento Médico"

    return AtendimentoStatusResponse(
        ativo=True,
        atendimento_id=atendimento.id,
        label_botao=label
    )


@router.post("/", response_model=AtendimentoResponse, status_code=201)
async def registrar_atendimento(
    payload: AtendimentoCreate, db: AsyncSession = Depends(get_db)
):
    """
    UC004 - Iniciar atendimento.
    Cria registro inicial (chegada) mediante validação geográfica.
    """
    # 1. Verifica se paciente existe
    paciente_result = await db.execute(select(Paciente).where(Paciente.id == payload.paciente_id))
    if paciente_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")

    # 2. Verifica se unidade existe e valida a distância geográfica
    unidade_result = await db.execute(select(Unidade).where(Unidade.id == payload.unidade_id))
    unidade = unidade_result.scalar_one_or_none()
    
    if unidade is None:
        raise HTTPException(status_code=404, detail="Unidade não encontrada.")

    # 2. Validação geográfica baseada na unidade atrelada ao atendimento
    ponto_paciente = func.ST_SetSRID(
        func.ST_MakePoint(payload.longitude, payload.latitude), 
        4326
    )

    # Executa a validação ST_DWithin no banco de dados
    distancia_valida_query = select(
        func.ST_DWithin(
            func.cast(Unidade.localizacao, Geography(geometry_type='POINT', srid=4326)),
            func.cast(ponto_paciente, Geography(geometry_type='POINT', srid=4326)),
            RAIO_PERMITIDO_METROS
        )
    ).where(Unidade.id == payload.unidade_id) # Atenção: no PATCH, use atendimento.unidade_id
    
    distancia_result = await db.execute(distancia_valida_query)
    is_within_radius = distancia_result.scalar()

    if not is_within_radius:
        raise HTTPException(
            status_code=403, 
            detail="Paciente fora do raio permitido para registrar entrada nesta unidade."
        )

    # 3. Verifica se já existe atendimento em aberto
    em_aberto_result = await db.execute(
        select(Atendimento).where(
            (Atendimento.paciente_id == payload.paciente_id)
            & (Atendimento.status == StatusAtendimento.em_aberto)
        )
    )
    if em_aberto_result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=409,
            detail="Já existe um atendimento em aberto para este paciente.",
        )

    # 4. Grava o horário de chegada
    novo_atendimento = Atendimento(
        paciente_id=payload.paciente_id,
        unidade_id=payload.unidade_id,
        status=StatusAtendimento.em_aberto,
        horario_chegada=datetime.now(),
        horario_triagem=None,
        horario_atendimento=None,
    )

    db.add(novo_atendimento)
    await db.commit()
    await db.refresh(novo_atendimento)

    return novo_atendimento


@router.patch("/{atendimento_id}/avancar-etapa", response_model=AtendimentoResponse)
async def avancar_etapa_atendimento(
    atendimento_id: int,
    payload: AtendimentoAvancar,
    db: AsyncSession = Depends(get_db),
):
    """
    UC004 - Avançar etapa do atendimento.
    Transiciona o estado cronológico mediante validação geográfica.
    """
    # 1. Busca o atendimento
    result = await db.execute(select(Atendimento).where(Atendimento.id == atendimento_id))
    atendimento: Atendimento | None = result.scalar_one_or_none()

    if atendimento is None:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado.")

    if atendimento.status == StatusAtendimento.concluido:
        raise HTTPException(status_code=409, detail="Este atendimento já foi concluído.")

    # 2. Validação geográfica baseada na unidade atrelada ao atendimento
    ponto_paciente = func.ST_SetSRID(
        func.ST_MakePoint(payload.longitude, payload.latitude), 
        4326
    )

    # Executa a validação ST_DWithin no banco de dados
    distancia_valida_query = select(
        func.ST_DWithin(
            func.cast(Unidade.localizacao, Geography(geometry_type='POINT', srid=4326)),
            func.cast(ponto_paciente, Geography(geometry_type='POINT', srid=4326)),
            RAIO_PERMITIDO_METROS
        )
    ).where(Unidade.id == atendimento.unidade_id)
    
    distancia_result = await db.execute(distancia_valida_query)
    is_within_radius = distancia_result.scalar()

    if not is_within_radius:
        raise HTTPException(
            status_code=403, 
            detail="Paciente fora do raio permitido para registrar o andamento nesta unidade."
        )

    # 3. Máquina de estado cronológica
    agora = datetime.now()

    if atendimento.horario_triagem is None:
        atendimento.horario_triagem = agora
    elif atendimento.horario_atendimento is None:
        atendimento.horario_atendimento = agora
        atendimento.status = StatusAtendimento.concluido
    else:
        # Fallback de segurança lógica
        raise HTTPException(status_code=422, detail="Todas as etapas de horário já foram registradas.")

    await db.commit()
    await db.refresh(atendimento)

    return atendimento


@router.get("/paciente/{paciente_id}", response_model=list[AtendimentoResponse])
async def listar_atendimentos_paciente(
    paciente_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    Lista o histórico completo de atendimentos de um paciente.
    Ordenado do mais recente para o mais antigo.
    """
    # 1. Verifica se o paciente existe
    paciente_query = select(Paciente).where(Paciente.id == paciente_id)
    paciente_result = await db.execute(paciente_query)
    if paciente_result.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=404, 
            detail="Paciente não encontrado."
        )

    # 2. Busca os atendimentos com ordenação decrescente por horário de chegada
    query = (
        select(Atendimento)
        .where(Atendimento.paciente_id == paciente_id)
        .order_by(desc(Atendimento.horario_chegada))
    )
    
    result = await db.execute(query)
    atendimentos = result.scalars().all()

    return atendimentos