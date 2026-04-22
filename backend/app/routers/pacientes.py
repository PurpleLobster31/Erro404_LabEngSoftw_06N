
# Este arquivo ainda não foi atualizado para usar o banco via docker

"""from fastapi import APIRouter, HTTPException
from backend.app.schemas.paciente import PacienteCreate, PacienteResponse
from backend.app import database

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.post("/", response_model=PacienteResponse, status_code=201)
def criar_paciente(payload: PacienteCreate):
    ""\"Cadastra um novo paciente.\"""
    for p in database.pacientes_db.values():
        if p["email"] == payload.email:
            raise HTTPException(status_code=409, detail="E-mail já cadastrado.")

    new_id = max(database.pacientes_db.keys(), default=0) + 1
    record = {
        "id": new_id,
        "nome": payload.nome,
        "sobrenome": payload.sobrenome,
        "email": payload.email,
        "data_nascimento": payload.data_nascimento,
    }
    database.pacientes_db[new_id] = record
    return record


@router.get("/{paciente_id}", response_model=PacienteResponse)
def get_paciente(paciente_id: int):
    ""\"Retorna dados de um paciente pelo ID.\"""
    paciente = database.pacientes_db.get(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")
    return paciente"""