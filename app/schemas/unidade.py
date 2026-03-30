from pydantic import BaseModel
from typing import Optional


class UnidadeBase(BaseModel):
    nome: str
    tipo: str
    endereco: str
    numero: str
    complemento: Optional[str] = None
    cep: str
    cidade: str
    estado: str
    telefone1: str
    telefone2: Optional[str] = None


class UnidadeCreate(UnidadeBase):
    pass


class UnidadeResponse(UnidadeBase):
    id: int
    tempo_medio_minutos: Optional[float] = None

    model_config = {"from_attributes": True}