from fastapi import APIRouter, HTTPException
from app.schemas.atendimento import (
    AtendimentoCreate,
    AtendimentoUpdate,
    AtendimentoResponse,
    StatusAtendimento,
)
from backend.app import database

router = APIRouter(prefix="/atendimentos", tags=["Atendimentos"])


@router.post("/", response_model=AtendimentoResponse, status_code=201)
def registrar_atendimento(payload: AtendimentoCreate) -> dict:
    
    if payload.paciente_id not in database.pacientes_db:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")
    if payload.unidade_id not in database.unidades_db:
        raise HTTPException(status_code=404, detail="Unidade não encontrada.")

    for at in database.atendimentos_db.values():
        if at["paciente_id"] == payload.paciente_id and at["status"] == StatusAtendimento.em_aberto:
            raise HTTPException(
                status_code=409,
                detail="Já existe um atendimento em aberto para este paciente.",
            )

    new_id = database.next_atendimento_id()
    status = (
        StatusAtendimento.concluido
        if payload.horario_atendimento
        else StatusAtendimento.em_aberto
    )

    record = {
        "id": new_id,
        "paciente_id": payload.paciente_id,
        "unidade_id": payload.unidade_id,
        "horario_chegada": payload.horario_chegada,
        "horario_triagem": payload.horario_triagem,
        "horario_atendimento": payload.horario_atendimento,
        "status": status,
    }
    database.atendimentos_db[new_id] = record
    return record


@router.patch("/{atendimento_id}", response_model=AtendimentoResponse)
def atualizar_atendimento(atendimento_id: int, payload: AtendimentoUpdate):
    record = database.atendimentos_db.get(atendimento_id)
    if not record:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado.")
    if record["status"] == StatusAtendimento.concluido:
        raise HTTPException(status_code=409, detail="Atendimento já está concluído.")

    if payload.horario_triagem:
        if payload.horario_triagem <= record["horario_chegada"]:
            raise HTTPException(
                status_code=422,
                detail="Horário de triagem deve ser posterior ao de chegada.",
            )
        record["horario_triagem"] = payload.horario_triagem

    if payload.horario_atendimento:
        if not record["horario_triagem"]:
            raise HTTPException(
                status_code=422,
                detail="Triagem deve ser registrada antes do atendimento médico.",
            )
        if payload.horario_atendimento <= record["horario_triagem"]:
            raise HTTPException(
                status_code=422,
                detail="Horário de atendimento deve ser posterior ao de triagem.",
            )
        record["horario_atendimento"] = payload.horario_atendimento
        record["status"] = StatusAtendimento.concluido  # UC004 - Fluxo Alternativo: conclusão

    return record


@router.get("/paciente/{paciente_id}", response_model=list[AtendimentoResponse])
def listar_atendimentos_paciente(paciente_id: int):
    """Lista todos os atendimentos de um paciente."""
    if paciente_id not in database.pacientes_db:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")
    return [a for a in database.atendimentos_db.values() if a["paciente_id"] == paciente_id]