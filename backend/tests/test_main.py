import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete, select

from backend.app.main import app
from backend.database.database import AsyncSessionLocal
from backend.database.models import Atendimento, Paciente, Unidade


TEST_UNIDADE_NOME = "Unidade Teste API"
TEST_PACIENTE_EMAIL = "teste.api@medtime.local"
TEST_LOCALIZACAO = "SRID=4326;POINT(-46.6300 -23.5500)"


pytestmark = pytest.mark.anyio


async def _cleanup_test_data(session):
    unidade_result = await session.execute(select(Unidade).where(Unidade.nome == TEST_UNIDADE_NOME))
    unidade = unidade_result.scalar_one_or_none()

    paciente_result = await session.execute(select(Paciente).where(Paciente.email == TEST_PACIENTE_EMAIL))
    paciente = paciente_result.scalar_one_or_none()

    if paciente is not None:
        await session.execute(delete(Atendimento).where(Atendimento.paciente_id == paciente.id))
        await session.delete(paciente)

    if unidade is not None:
        await session.execute(delete(Atendimento).where(Atendimento.unidade_id == unidade.id))
        await session.delete(unidade)

    await session.commit()


async def _ensure_test_data():
    async with AsyncSessionLocal() as session:
        await _cleanup_test_data(session)

        unidade = Unidade(
            nome=TEST_UNIDADE_NOME,
            tipo="Hospital",
            endereco="Rua Teste",
            numero="123",
            complemento="Bloco A",
            cep="00000-000",
            cidade="Sao Paulo",
            estado="SP",
            telefone1="(11) 0000-0000",
            telefone2=None,
            descricao="Unidade criada para testes automatizados.",
            horario_funcionamento="24 horas",
            imagem_url=None,
            localizacao=TEST_LOCALIZACAO,
        )

        paciente = Paciente(
            nome="Teste",
            sobrenome="Automatizado",
            email=TEST_PACIENTE_EMAIL,
        )

        session.add_all([unidade, paciente])
        await session.commit()
        await session.refresh(unidade)
        await session.refresh(paciente)

        return unidade.id, paciente.id


async def _clear_atendimentos(paciente_id):
    async with AsyncSessionLocal() as session:
        await session.execute(delete(Atendimento).where(Atendimento.paciente_id == paciente_id))
        await session.commit()


@pytest.fixture(scope="module")
async def client_and_ids():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as test_client:
        unidade_id, paciente_id = await _ensure_test_data()
        yield test_client, {"unidade_id": unidade_id, "paciente_id": paciente_id}


@pytest.fixture
def client(client_and_ids):
    return client_and_ids[0]


@pytest.fixture
def test_ids(client_and_ids):
    return client_and_ids[1]


async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "MedTime API"}


async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_listar_unidades_retorna_lista(client, test_ids):
    response = await client.get("/unidades/")
    assert response.status_code == 200
    data = response.json()
    assert any(item["id"] == test_ids["unidade_id"] for item in data)
    unidade = next(item for item in data if item["id"] == test_ids["unidade_id"])
    assert unidade["nome"] == TEST_UNIDADE_NOME
    assert "latitude" in unidade
    assert "longitude" in unidade


async def test_listar_unidades_com_filtro_geografico(client, test_ids):
    response = await client.get("/unidades/?lat=-23.55&lon=-46.63&raio_km=2")
    assert response.status_code == 200
    data = response.json()
    assert any(item["id"] == test_ids["unidade_id"] for item in data)
    assert all("id" in unidade for unidade in data)


async def test_obter_unidade_por_id(client, test_ids):
    response = await client.get(f"/unidades/{test_ids['unidade_id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_ids["unidade_id"]
    assert data["nome"] == TEST_UNIDADE_NOME


async def test_obter_unidade_inexistente_retorna_404(client):
    response = await client.get("/unidades/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Unidade não encontrada"}


async def test_unidades_query_param_invalido_retorna_422(client):
    response = await client.get("/unidades/?lat=abc")
    assert response.status_code == 422


async def test_buscar_atendimento_ativo_sem_registro(client, test_ids):
    await _clear_atendimentos(test_ids["paciente_id"])

    response = await client.get(
        "/atendimentos/ativo",
        params={
            "paciente_id": test_ids["paciente_id"],
            "unidade_id": test_ids["unidade_id"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["ativo"] is False
    assert data["label_botao"] == "Registrar Entrada"
    assert data.get("atendimento_id") is None


async def test_registrar_atendimento_fora_do_raio(client, test_ids):
    await _clear_atendimentos(test_ids["paciente_id"])

    response = await client.post(
        "/atendimentos/",
        json={
            "paciente_id": test_ids["paciente_id"],
            "unidade_id": test_ids["unidade_id"],
            "latitude": 0.0,
            "longitude": 0.0,
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"].startswith("Paciente fora do raio")


async def test_fluxo_atendimento_completo(client, test_ids):
    await _clear_atendimentos(test_ids["paciente_id"])

    payload = {
        "paciente_id": test_ids["paciente_id"],
        "unidade_id": test_ids["unidade_id"],
        "latitude": -23.55,
        "longitude": -46.63,
    }

    response = await client.post("/atendimentos/", json=payload)
    assert response.status_code == 201
    atendimento = response.json()
    atendimento_id = atendimento["id"]

    status_response = await client.get(
        "/atendimentos/ativo",
        params={
            "paciente_id": test_ids["paciente_id"],
            "unidade_id": test_ids["unidade_id"],
        },
    )
    assert status_response.status_code == 200
    assert status_response.json()["label_botao"] == "Registrar Triagem"

    avancar = await client.patch(f"/atendimentos/{atendimento_id}/avancar-etapa", json=payload)
    assert avancar.status_code == 200
    assert avancar.json()["horario_triagem"] is not None
    assert avancar.json()["status"] == "em_aberto"

    status_response = await client.get(
        "/atendimentos/ativo",
        params={
            "paciente_id": test_ids["paciente_id"],
            "unidade_id": test_ids["unidade_id"],
        },
    )
    assert status_response.status_code == 200
    assert status_response.json()["label_botao"] == "Registrar Atendimento Médico"

    avancar = await client.patch(f"/atendimentos/{atendimento_id}/avancar-etapa", json=payload)
    assert avancar.status_code == 200
    assert avancar.json()["horario_atendimento"] is not None
    assert avancar.json()["status"] == "concluido"

    status_response = await client.get(
        "/atendimentos/ativo",
        params={
            "paciente_id": test_ids["paciente_id"],
            "unidade_id": test_ids["unidade_id"],
        },
    )
    assert status_response.status_code == 200
    assert status_response.json()["ativo"] is False

