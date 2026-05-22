# MedTime — Monitoramento de Tempo de Espera em Hospitais

MedTime e uma aplicacao para monitorar tempo medio de espera em unidades de pronto atendimento e registrar eventos de atendimento em tempo real. O sistema combina backend FastAPI, frontend Angular e banco PostgreSQL com PostGIS para consultas geoespaciais e validacao de proximidade.

Feito por:
* Beatriz Bellini Prado Garcia - 10419741
* Fabio Oliveira da Silva - 10420458
* Mateus Teles Magalhães - 10427410
* Matheus Mendonça Lopes - 10443495
* Patrick Rocha de Andrade - 10410902

Prof. Luiz Carlos Machi Lozano

## Objetivo e escopo

- Entregar tempos medios de espera por unidade (baseado nos ultimos 5 atendimentos).
- Permitir registro de etapas do atendimento com validacao de raio geografico.
- Disponibilizar busca textual de unidades no frontend.

Os casos de uso detalhados estao em [docs/UC001.md](docs/UC001.md), [docs/UC004.md](docs/UC004.md) e [docs/UC008.md](docs/UC008.md).

## Arquitetura (visao tecnica)

**Camadas logicas**
- **Apresentacao**: Angular 21 (standalone components), responsavel por listagem, detalhes de unidade, registro de etapas e busca textual.
- **Aplicacao**: FastAPI com rotas REST, validacao de regras de negocio e orquestracao das consultas geoespaciais.
- **Dados**: PostgreSQL 15 + PostGIS para persistencia e funcoes de distancia.

**Fluxo principal**
1. O frontend consulta `GET /unidades` e recebe tempos medios e coordenadas.
2. O backend calcula o tempo medio de triagem e atendimento com CTEs (ultimos 5 atendimentos por unidade).
3. Ao registrar etapas, o backend valida proximidade via `ST_DWithin` antes de gravar.

**Infraestrutura**
- Em desenvolvimento local, o ambiente usa Docker Compose com tres servicos (db, backend, frontend).
- O deployment alvo e uma instancia unica na AWS (EC2) com containers e reverse proxy, conforme [docs/arquitetura.md](docs/arquitetura.md).

## Stack e componentes

**Backend**
- FastAPI com routers para unidades e atendimentos.
- SQLAlchemy async + Alembic para ORM e migracoes.
- GeoAlchemy2 + PostGIS para distancia e geolocalizacao.

**Frontend**
- Angular 21 (standalone), com paginas para lista e detalhe de unidades, registro de atendimento e historico.

**Banco**
- PostgreSQL 15 + PostGIS.

## Estrutura relevante do repositorio

- Backend e API: [backend/app](backend/app)
- Routers principais: [backend/app/routers](backend/app/routers)
- Modelos e conexao DB: [backend/database](backend/database)
- Migracoes: [alembic](alembic)
- Frontend Angular: [frontend](frontend)
- Documentacao: [docs](docs)
- Testes automatizados: [backend/tests](backend/tests)
- Pipeline CI: [.github/workflows/ci.yml](.github/workflows/ci.yml)

## Backend — detalhes tecnicos

**Rotas principais**
- `GET /unidades`: lista unidades com tempos medios e, se informado `lat`, `lon` e `raio_km`, aplica filtro e ordenacao por distancia.
- `GET /unidades/{id}`: detalha uma unidade com tempo medio total.
- `GET /atendimentos/ativo`: verifica atendimento em aberto e devolve o estado do botao.
- `POST /atendimentos`: cria o registro inicial (chegada) com validacao de raio.
- `PATCH /atendimentos/{id}/avancar-etapa`: avanca para triagem e atendimento medico.
- `GET /atendimentos/paciente/{paciente_id}`: lista historico ordenado por data.
- `GET /health`: health check simples.

**Calculo de tempo medio**
- Para cada unidade, o backend calcula media de triagem e de atendimento com janela dos ultimos 5 registros.
- A soma das medias forma o tempo medio total exibido no frontend.

**Geolocalizacao**
- A validacao de proximidade usa `ST_DWithin` com cast para `Geography` (metros).
- O raio permitido e 2 km.

**Seed de dados**
- Na inicializacao do backend, o seed popula unidades, pacientes e atendimentos de exemplo.
- Paciente de teste do frontend: ID `999`.

## Frontend — detalhes tecnicos

**Organizacao**
- Paginas principais em [frontend/src/app/pages](frontend/src/app/pages).
- Servicos de dados e geolocalizacao em [frontend/src/app/core](frontend/src/app/core).

**Fluxos implementados**
- Lista de unidades com tempo medio (UC001).
- Detalhe da unidade com botao dinamico de registro (UC004).
- Busca textual de hospitais (UC008).

**Geolocalizacao (modo mock)**
- Para demonstracao sem GPS real, use `?geoloc-mock=true` na URL do frontend.

## Banco de dados e modelo

- Entidades principais: Unidade, Paciente, Atendimento.
- Relacionamentos: Unidade 1..* Atendimento, Paciente 1..* Atendimento.
- Detalhes do modelo em [docs/dominio_classes.md](docs/dominio_classes.md).

## Instalacao e execucao

### 1) Executar tudo via Docker (recomendado)

```bash
docker-compose up -d
```

O banco leva alguns segundos para ficar pronto. Aguarde ~15s antes de fazer migracoes ou testes.

**Acessos locais**
- Frontend: http://localhost:4200
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

### 2) Execucao local (backend fora do container)

1. Suba o banco via Docker:
```bash
docker-compose up -d db
```

2. Crie o ambiente virtual e instale dependencias:
```bash
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements-dev.txt
```

3. Aplique migracoes:
```bash
python -m alembic upgrade head
```

4. Inicie a API:
```bash
uvicorn backend.app.main:app --reload
```

### 3) Frontend local

```bash
cd frontend
npm ci
npm run start
```

O proxy local usa `/api` e encaminha para o backend.

## Configuracao e variaveis

Variaveis default do Docker Compose:
- `POSTGRES_USER`: `dev_user`
- `POSTGRES_PASSWORD`: `dev_password`
- `POSTGRES_DB`: `app_db`
- `DATABASE_URL`: `postgresql+asyncpg://dev_user:dev_password@db:5432/app_db`

Regras adicionais e observacoes de PostGIS estao em [CONFIG-DE-AMBIENTE.md](CONFIG-DE-AMBIENTE.md).

## Testes e validacao

**Automatizados**
- Rodar testes com banco PostGIS:
```bash
docker-compose up -d
python -m alembic upgrade head
python -m pytest
```

**CI**
- O pipeline esta definido em [.github/workflows/ci.yml](.github/workflows/ci.yml) e executa migracoes e testes com cobertura (minimo 70%).

Plano de testes completo em [TESTES.md](TESTES.md).

## Documentacao do projeto

- Arquitetura e deploy alvo: [docs/arquitetura.md](docs/arquitetura.md)
- Requisitos: [docs/Lista_Requisitos.md](docs/Lista_Requisitos.md)
- Casos de uso: [docs/UC001.md](docs/UC001.md), [docs/UC004.md](docs/UC004.md), [docs/UC008.md](docs/UC008.md)
- Diagrama de casos de uso: [docs/Diagrama_casos_uso.md](docs/Diagrama_casos_uso.md)
- Diagrama de dominio: [docs/dominio_classes.md](docs/dominio_classes.md)

## Deploy (alvo do projeto)

O deploy previsto utiliza uma unica instancia EC2 executando containers:
1. Build das imagens (backend, frontend e PostGIS).
2. Subida com Docker Compose.
3. Reverse proxy (ex.: Nginx) para servir frontend e encaminhar `/api` ao backend.
4. Ajuste de variaveis e HTTPS em producao.