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

## Casos de teste manuais (frontend)

| ID | Caso | Passos | Resultado esperado | UC |
| --- | --- | --- | --- | --- |
| CT-FE-001 | Busca textual por hospital existente | Acessar lista de unidades, digitar um nome valido e buscar | Lista filtrada com a unidade correspondente | UC008 |
| CT-FE-002 | Busca sem resultados | Pesquisar termo inexistente | Mensagem de "nenhum hospital encontrado" e campo permanece editavel | UC008 |

## Evidencias solicitadas pelo professor
- Video curto (sem audio) mostrando a esteira rodando testes automatizados.
- Capturas de tela da execucao dos testes (prints) para anexar no .docx.
