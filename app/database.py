from datetime import datetime
from typing import Dict

# --- Unidades de saúde ---
unidades_db: Dict[int, dict] = {
    1: {
        "id": 1,
        "nome": "UPA Central",
        "tipo": "UPA",
        "endereco": "Rua das Flores, 100",
        "cidade": "São Paulo",
        "estado": "SP",
        "telefone1": "11-1234-5678",
        "tempo_medio_minutos": 45.0,
    },
    2: {
        "id": 2,
        "nome": "Hospital Municipal Norte",
        "tipo": "Hospital",
        "endereco": "Av. Norte, 500",
        "cidade": "São Paulo",
        "estado": "SP",
        "telefone1": "11-9876-5432",
        "tempo_medio_minutos": 90.0,
    },
}

# --- Pacientes ---
pacientes_db: Dict[int, dict] = {
    1: {
        "id": 1,
        "nome": "João",
        "sobrenome": "Silva",
        "email": "joao@email.com",
    }
}

# --- Atendimentos ---
atendimentos_db: Dict[int, dict] = {}
_atendimento_id_counter = 1


def next_atendimento_id() -> int:
    global _atendimento_id_counter
    _atendimento_id_counter += 1
    return _atendimento_id_counter