from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class PacienteCreate(BaseModel):
    nome: str
    sobrenome: str
    data_nascimento: date
    email: EmailStr
    senha: str


class PacienteResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    email: str
    data_nascimento: date

    model_config = {"from_attributes": True}