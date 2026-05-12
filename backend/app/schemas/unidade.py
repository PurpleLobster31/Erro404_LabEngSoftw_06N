from pydantic import BaseModel
from typing import Optional

class UnidadeBase(BaseModel):
    nome: str
    tipo: str
    endereco: str
    numero: Optional[str] = None
    complemento: Optional[str] = None
    cep: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    telefone1: Optional[str] = None
    telefone2: Optional[str] = None
    descricao: Optional[str] = None
    horario_funcionamento: Optional[str] = None

class UnidadeCreate(UnidadeBase):
    # Latitude e longitude são necessárias para montar o POINT no banco na hora da criação
    latitude: float
    longitude: float

class UnidadeResponse(UnidadeBase):
    id: int
    tempo_medio_minutos: Optional[float] = None # Calculado dinamicamente no router

    class Config:
        from_attributes = True