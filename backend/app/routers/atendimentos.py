from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta

from backend.database.database import get_db
from backend.database.models import Atendimento, Paciente, Unidade
from backend.app.schemas.atendimento import (
    AtendimentoCreate,
    AtendimentoUpdate,
    AtendimentoResponse,
    StatusAtendimento,
    AtendimentoGet,
    AtendimentoStatusResponse
)

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
    UC004 - Registrar evento de atendimento
    Cria um novo atendimento com validação de cronologia.
    Status: concluído se todos os horários forem preenchidos, caso contrário em_aberto.
    """
    # Verifica se paciente existe
    paciente_result = await db.execute(select(Paciente).where(Paciente.id == payload.paciente_id))
    if paciente_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")

    # Verifica se unidade existe
    unidade_result = await db.execute(select(Unidade).where(Unidade.id == payload.unidade_id))
    if unidade_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Unidade não encontrada.")

    # Verifica se já existe atendimento em aberto para este paciente
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

    # Determina status baseado se todos os campos foram preenchidos
    status = (
        StatusAtendimento.concluido
        if payload.horario_atendimento is not None
        else StatusAtendimento.em_aberto
    )

    novo_atendimento = Atendimento(
        paciente_id=payload.paciente_id,
        unidade_id=payload.unidade_id,
        horario_chegada=payload.horario_chegada,
        horario_triagem=payload.horario_triagem,
        horario_atendimento=payload.horario_atendimento,
        status=status,
    )

    db.add(novo_atendimento)
    await db.commit()
    await db.refresh(novo_atendimento)

    return novo_atendimento


@router.put("/{atendimento_id}", response_model=AtendimentoResponse)
async def atualizar_atendimento(
    atendimento_id: int,
    payload: AtendimentoUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    UC004 - Atualizar evento de atendimento (salvar parcial)
    Permite atualizar horários individuais com validação de cronologia.
    Transiciona para concluído quando horario_atendimento é preenchido.
    """
    # Busca o atendimento
    result = await db.execute(
        select(Atendimento).where(Atendimento.id == atendimento_id)
    )
    atendimento: Atendimento | None = result.scalar_one_or_none()

    if atendimento is None:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado.")

    # Não permite atualização se já concluído
    if atendimento.status == StatusAtendimento.concluido:
        raise HTTPException(status_code=409, detail="Atendimento já está concluído.")

    # Valida e atualiza horário de triagem
    if payload.horario_triagem is not None:
        # Garante que o horário base existe antes da comparação
        if atendimento.horario_chegada is None:
            raise HTTPException(
                status_code=422,
                detail="Não é possível registrar triagem sem um horário de chegada.",
            )
            
        if payload.horario_triagem <= atendimento.horario_chegada:
            raise HTTPException(
                status_code=422,
                detail="Horário de triagem deve ser posterior ao de chegada.",
            )
        atendimento.horario_triagem = payload.horario_triagem

    # Valida e atualiza horário de atendimento
    if payload.horario_atendimento is not None:
        # Garante que o horário base existe antes da comparação
        if atendimento.horario_triagem is None:
            raise HTTPException(
                status_code=422,
                detail="Triagem deve ser registrada antes do atendimento médico.",
            )
            
        if payload.horario_atendimento <= atendimento.horario_triagem:
            raise HTTPException(
                status_code=422,
                detail="Horário de atendimento deve ser posterior ao de triagem.",
            )
        atendimento.horario_atendimento = payload.horario_atendimento
        # UC004 - Fluxo Alternativo: transiciona para concluído
        atendimento.status = StatusAtendimento.concluido

    await db.commit()
    await db.refresh(atendimento)

    return atendimento


@router.get("/paciente/{paciente_id}", response_model=list[AtendimentoResponse])
async def listar_atendimentos_paciente(
    paciente_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Lista todos os atendimentos de um paciente.
    """
    # Verifica se paciente existe
    paciente_result = await db.execute(select(Paciente).where(Paciente.id == paciente_id))
    if paciente_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")

    # Busca atendimentos
    result = await db.execute(
        select(Atendimento).where(Atendimento.paciente_id == paciente_id)
    )
    atendimentos = result.scalars().all()

    return atendimentos