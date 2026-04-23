import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.database.database import get_db


class _FakeMappings:
    def __init__(self, rows):
        self._rows = rows

    def all(self):
        return self._rows


class _FakeResult:
    def __init__(self, rows):
        self._rows = rows

    def mappings(self):
        return _FakeMappings(self._rows)


class _FakeAsyncSession:
    def __init__(self, rows):
        self._rows = rows

    async def execute(self, _query):
        return _FakeResult(self._rows)


@pytest.fixture
def client():
    rows = [
        {
            "id": 1,
            "nome": "UPA Centro",
            "endereco": "Rua A, 100",
            "tempo_medio_minutos": 45.0,
            "latitude": -23.55,
            "longitude": -46.63,
        },
        {
            "id": 2,
            "nome": "Hospital Municipal",
            "endereco": "Av. B, 200",
            "tempo_medio_minutos": 30.0,
            "latitude": -23.56,
            "longitude": -46.64,
        },
    ]

    async def _override_get_db():
        yield _FakeAsyncSession(rows)

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "MedTime API"}


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_listar_unidades_retorna_lista(client):
    response = client.get("/unidades/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["nome"] == "UPA Centro"
    assert "latitude" in data[0]
    assert "longitude" in data[0]


def test_listar_unidades_com_filtro_geografico(client):
    response = client.get("/unidades/?lat=-23.55&lon=-46.63&raio_km=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all("id" in unidade for unidade in data)