from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class StatusAtendimento(str, Enum):
    em_aberto = "em_aberto"
    concluido = "concluido"


class AtendimentoCreate(BaseModel):
    paciente_id: int
    unidade_id: int
    horario_chegada: datetime
    horario_triagem: Optional[datetime] = None
    horario_atendimento: Optional[datetime] = None

    @model_validator(mode="after")
    def validar_ordem_cronologica(self):
        """UC004 - Fluxo de Exceção 1: garante Chegada < Triagem < Atendimento."""
        if self.horario_triagem and self.horario_triagem <= self.horario_chegada:
            raise ValueError("Horário de triagem deve ser posterior ao de chegada.")
        if self.horario_atendimento:
            if not self.horario_triagem:
                raise ValueError("Triagem deve ser registrada antes do atendimento.")
            if self.horario_atendimento <= self.horario_triagem:
                raise ValueError("Horário de atendimento deve ser posterior ao de triagem.")
        return self


class AtendimentoUpdate(BaseModel):
    horario_triagem: Optional[datetime] = None
    horario_atendimento: Optional[datetime] = None


class AtendimentoResponse(BaseModel):
    id: int
    paciente_id: int
    unidade_id: int
    horario_chegada: datetime
    horario_triagem: Optional[datetime] = None
    horario_atendimento: Optional[datetime] = None
    status: StatusAtendimento

    model_config = {"from_attributes": True}