import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import database

client = TestClient(app)


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_atendimentos():
    """Limpa atendimentos entre testes para garantir isolamento."""
    database.atendimentos_db.clear()
    database._atendimento_id_counter = 1
    yield


# ── Health ───────────────────────────────────────────────────────────────────

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ── UC001 / UC008 - Unidades ─────────────────────────────────────────────────

def test_listar_unidades():
    response = client.get("/unidades/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_unidade_existente():
    response = client.get("/unidades/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_unidade_inexistente():
    response = client.get("/unidades/999")
    assert response.status_code == 404


def test_pesquisar_unidade_por_nome():
    """UC008 - Pesquisar Hospitais por nome."""
    response = client.get("/unidades/?nome=UPA")
    assert response.status_code == 200
    resultados = response.json()
    assert all("UPA" in u["nome"] for u in resultados)


def test_pesquisar_unidade_sem_resultado():
    """UC008 - Busca Sem Resultados."""
    response = client.get("/unidades/?nome=HospitalInexistente")
    assert response.status_code == 404


# ── UC004 - Registrar Atendimento ────────────────────────────────────────────

PAYLOAD_BASE = {
    "paciente_id": 1,
    "unidade_id": 1,
    "horario_chegada": "2024-06-01T08:00:00",
}


def test_registrar_atendimento_sucesso():
    """UC004 - Fluxo Principal: cria atendimento em aberto."""
    response = client.post("/atendimentos/", json=PAYLOAD_BASE)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "em_aberto"
    assert data["horario_triagem"] is None


def test_registrar_atendimento_sem_unidade_invalida():
    """UC004 - Exceção 2: unidade não existe."""
    payload = {**PAYLOAD_BASE, "unidade_id": 999}
    response = client.post("/atendimentos/", json=payload)
    assert response.status_code == 404


def test_registrar_atendimento_ordem_cronologica_invalida():
    """UC004 - Exceção 1: triagem antes da chegada."""
    payload = {
        **PAYLOAD_BASE,
        "horario_triagem": "2024-06-01T07:00:00",  # antes da chegada
    }
    response = client.post("/atendimentos/", json=payload)
    assert response.status_code == 422


def test_atualizar_atendimento_com_triagem():
    """UC004 - Fluxo Principal: adiciona triagem ao atendimento em aberto."""
    client.post("/atendimentos/", json=PAYLOAD_BASE)
    response = client.patch(
        "/atendimentos/2",
        json={"horario_triagem": "2024-06-01T09:00:00"},
    )
    assert response.status_code == 200
    assert response.json()["horario_triagem"] is not None
    assert response.json()["status"] == "em_aberto"


def test_concluir_atendimento():
    """UC004 - Fluxo Alternativo: conclui ao registrar horário de atendimento médico."""
    client.post("/atendimentos/", json={
        **PAYLOAD_BASE,
        "horario_triagem": "2024-06-01T09:00:00",
    })
    response = client.patch(
        "/atendimentos/2",
        json={"horario_atendimento": "2024-06-01T10:00:00"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "concluido"


def test_atendimento_duplicado_bloqueado():
    """UC004: não permite dois atendimentos em aberto para o mesmo paciente."""
    client.post("/atendimentos/", json=PAYLOAD_BASE)
    response = client.post("/atendimentos/", json=PAYLOAD_BASE)
    assert response.status_code == 409