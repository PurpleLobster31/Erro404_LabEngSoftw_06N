from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class StatusAtendimento(str, Enum):
    em_aberto = "em_aberto"
    concluido = "concluido"


class CoordenadasPayload(BaseModel):
    latitude: float
    longitude: float

class AtendimentoCreate(CoordenadasPayload):
    paciente_id: int
    unidade_id: int

class AtendimentoAvancar(CoordenadasPayload):
    pass


class AtendimentoResponse(BaseModel):
    id: int
    paciente_id: int
    unidade_id: int
    horario_chegada: datetime
    horario_triagem: Optional[datetime] = None
    horario_atendimento: Optional[datetime] = None
    status: StatusAtendimento

    model_config = {"from_attributes": True}

class AtendimentoGet(BaseModel):
    paciente_id: int
    unidade_id: int

class AtendimentoStatusResponse(BaseModel):
    ativo: bool
    atendimento_id: int | None = None
    label_botao: str