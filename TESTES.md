# Plano de Testes - MedTime

## Objetivo
Validar o fluxo principal da API (UC001 e UC004) com testes automatizados contra banco real PostGIS e documentar o roteiro manual do UC008 (frontend).

## Escopo
- API FastAPI: unidades e atendimentos.
- Banco de dados: Postgres 15 + PostGIS com migracoes aplicadas.
- Frontend: busca textual (UC008) com validacao manual.

## Ambiente e dependencias
- Python 3.12
- PostgreSQL 15 + PostGIS
- Migracoes Alembic aplicadas
- Variavel de ambiente `DATABASE_URL` apontando para o Postgres

## Como executar os testes automatizados
1. Subir o banco de dados com Docker:
   ```bash
   docker-compose up -d
   ```
2. Aplicar migracoes:
   ```bash
   python -m alembic upgrade head
   ```
3. Rodar os testes:
   ```bash
   python -m pytest
   ```

## Execucao na esteira (CI)
A esteira usa o workflow definido em [/.github/workflows/ci.yml](.github/workflows/ci.yml) e executa os passos abaixo em ambiente Linux :

1. Sobe um Postgres + PostGIS como servico do GitHub Actions.
2. Instala as dependencias Python.
3. Executa migracoes Alembic com `DATABASE_URL` apontando para `localhost:5432`.
4. Roda os testes com cobertura e falha se o total ficar abaixo de 70%:
   ```bash
   python -m pytest --cov=backend.app --cov-config=.coveragerc --cov-report=term-missing --cov-report=xml --cov-fail-under=70
   ```
5. Publica o `coverage.xml` como artefato do job.

## Casos de teste automatizados (API)

| ID | Caso | Endpoint | Resultado esperado | UC |
| --- | --- | --- | --- | --- |
| CT-API-001 | Health check responde OK | `GET /health` | `200` e `{ "status": "ok" }` | - |
| CT-API-002 | Lista de unidades inclui unidade de teste | `GET /unidades/` | `200` e retorno contem unidade criada no setup | UC001 |
| CT-API-003 | Filtro geografico retorna unidade no raio | `GET /unidades/?lat=-23.55&lon=-46.63&raio_km=2` | `200` e retorno contem unidade no raio | UC001 |
| CT-API-004 | Detalhe de unidade existente | `GET /unidades/{id}` | `200` com dados completos | UC001 |
| CT-API-005 | Unidade inexistente retorna 404 | `GET /unidades/999` | `404` com mensagem de erro | UC001 |
| CT-API-006 | Parametro invalido retorna 422 | `GET /unidades/?lat=abc` | `422` | UC001 |
| CT-API-007 | Sem atendimento ativo | `GET /atendimentos/ativo` | `200`, `ativo=false`, label "Registrar Entrada" | UC004 |
| CT-API-008 | Registro de entrada fora do raio | `POST /atendimentos` | `403` com mensagem de raio permitido | UC004 |
| CT-API-009 | Fluxo completo de atendimento | `POST /atendimentos` + `PATCH /atendimentos/{id}/avancar-etapa` | `201` e transicoes ate `concluido` | UC004 |
| CT-API-010 | Paciente inexistente ao registrar | `POST /atendimentos` | `404` "Paciente nao encontrado" | UC004 |
| CT-API-011 | Unidade inexistente ao registrar | `POST /atendimentos` | `404` "Unidade nao encontrada" | UC004 |
| CT-API-012 | Atendimento em aberto bloqueia nova entrada | `POST /atendimentos` | `409` conflito | UC004 |
| CT-API-013 | Avancar etapa inexistente | `PATCH /atendimentos/{id}/avancar-etapa` | `404` "Atendimento nao encontrado" | UC004 |
| CT-API-014 | Avancar em atendimento concluido | `PATCH /atendimentos/{id}/avancar-etapa` | `409` "Atendimento ja concluido" | UC004 |
| CT-API-015 | Avancar fora do raio permitido | `PATCH /atendimentos/{id}/avancar-etapa` | `403` com mensagem de raio | UC004 |
| CT-API-016 | Avancar com todas as etapas preenchidas | `PATCH /atendimentos/{id}/avancar-etapa` | `422` com mensagem de etapas registradas | UC004 |
| CT-API-017 | Historico ordenado por data | `GET /atendimentos/paciente/{id}` | `200` com lista ordenada desc | UC004 |
| CT-API-018 | Historico para paciente inexistente | `GET /atendimentos/paciente/999` | `404` "Paciente nao encontrado" | UC004 |

## Casos de teste manuais (frontend)

| ID | Caso | Passos | Resultado esperado | UC |
| --- | --- | --- | --- | --- |
| CT-FE-001 | Busca textual por hospital existente | Acessar lista de unidades, digitar um nome valido e buscar | Lista filtrada com a unidade correspondente | UC008 |
| CT-FE-002 | Busca sem resultados | Pesquisar termo inexistente | Mensagem de "nenhum hospital encontrado" e campo permanece editavel | UC008 |

