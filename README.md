# MedTime — Monitoramento de Tempo de Espera em Hospitais

MedTime é uma aplicação que ajuda pacientes a visualizar tempos médios de espera em unidades de pronto atendimento e registrar etapas do atendimento em tempo real. O projeto está organizado em backend FastAPI, frontend Angular e banco PostgreSQL com PostGIS para geolocalização.

## Visão geral do funcionamento

1. O frontend Angular lista unidades e seus tempos médios de espera.
2. A API FastAPI consulta o banco com dados de atendimento e calcula tempos médios (últimos 5 registros).
3. O paciente pode registrar entrada, triagem e atendimento médico em etapas, com validação de proximidade geográfica.

## Casos de uso implementados

- **UC001 — Verificar Tempo em Pronto Atendimento**  
  Listagem de unidades com tempo médio de espera e ordenação por proximidade quando a geolocalização está disponível.

- **UC004 — Registrar evento de atendimento (fluxo síncrono)**  
  Registro por etapas (entrada → triagem → atendimento médico) com botão dinâmico e validação de raio (2 km).

- **UC008 — Pesquisar Hospitais**  
  Busca textual na lista de unidades, filtrando por nome e endereço no frontend.

**Em evolução / mockados:** histórico de atendimentos, avaliações, favoritos e perfil do paciente estão representados no frontend como placeholders/mocks para próximas etapas.

## Tecnologias

**Backend**
- Python + FastAPI (API REST)
- SQLAlchemy async + Alembic (ORM e migrações)
- GeoAlchemy2 + PostGIS (geolocalização e cálculo de distância)

**Frontend**
- Angular 21 (standalone components)

**Banco de dados**
- PostgreSQL 15 + PostGIS

**Infra**
- Docker + Docker Compose
- **Deploy alvo: EC2** (frontend, backend e banco hospedados na mesma instância)

## Principais endpoints da API

- `GET /unidades` — Lista unidades (suporta `lat`, `lon`, `raio_km` para proximidade)
- `GET /unidades/{id}` — Detalhes de uma unidade e tempo médio calculado
- `GET /atendimentos/ativo` — Status do atendimento ativo (para controle do botão)
- `POST /atendimentos` — Registrar entrada
- `PATCH /atendimentos/{id}/avancar-etapa` — Registrar triagem/atendimento médico
- `GET /atendimentos/paciente/{paciente_id}` — Histórico do paciente
- `GET /health` — Health check

## Executar localmente (Docker)

```bash
docker-compose up -d
sleep 15
```

**Acessos locais:**
- Frontend: http://localhost:4200
- API: http://localhost:8000
- Docs da API: http://localhost:8000/docs

**Proxy local do frontend:** o Angular usa `/api` como base e o `frontend/proxy.conf.json` encaminha para o backend no Docker.

## Dados iniciais

No startup da API, um seed popula o banco com unidades, pacientes e atendimentos de exemplo. O paciente de teste usado no frontend possui ID `999`.

## Variáveis de ambiente padrão (docker-compose.yml)

- `POSTGRES_USER`: `dev_user`
- `POSTGRES_PASSWORD`: `dev_password`
- `POSTGRES_DB`: `app_db`
- `DATABASE_URL`: `postgresql+asyncpg://dev_user:dev_password@db:5432/app_db`

## Geolocalização (modo mock)

Para demonstrar o fluxo de registro sem GPS real, use `?geoloc-mock=true` na URL do frontend. O botão de registro ficará habilitado e a localização será simulada.

## Deploy no EC2 (alvo do projeto)

O projeto foi pensado para publicar **todos os serviços em uma instância EC2** utilizando Docker:

1. Build das imagens (backend, frontend e PostGIS).
2. Execução com Docker Compose na instância.
3. Configurar reverse proxy (ex.: Nginx) para servir o frontend e encaminhar `/api` para o backend.
4. Ajustar variáveis de ambiente para produção e habilitar HTTPS.

## Estrutura do projeto

```
.
├── backend/              # API FastAPI
├── frontend/             # Angular 21
├── alembic/              # Migrações
├── docker-compose.yml    # Ambiente local e EC2
└── README.md
```

## Documentação

- Casos de uso: [docs/UC001.md](docs/UC001.md), [docs/UC004.md](docs/UC004.md), [docs/UC008.md](docs/UC008.md)
- Arquitetura: [docs/arquitetura.md](docs/arquitetura.md)
- Requisitos: [docs/Lista_Requisitos.md](docs/Lista_Requisitos.md)
- Testes: [TESTES.md](TESTES.md)

## Testes automatizados

1. Subir o banco de dados:

```bash
docker-compose up -d
```

2. Rodar migracoes:

```bash
python -m alembic upgrade head
```

3. Executar a suite:

```bash
python -m pytest
```