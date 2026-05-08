# MedTime - Aplicação de Tempo de Espera em Hospitais

Backend FastAPI + Frontend Angular + Banco de dados PostgreSQL.

## Início Rápido

### Pré-requisitos
- Docker e Docker Compose instalados
- Git

### Executar Localmente

```bash
# Clonar e entrar no repositório
git clone <url-repo>
cd Erro404_LabEngSoftw_06N

# Iniciar todos os serviços
docker-compose up -d

# Aguarde ~15 segundos para as migrações serem concluídas
sleep 15

# Verificar se os serviços estão rodando
curl http://localhost:8000/health    # Backend
curl http://localhost:4200            # Frontend (no navegador)
```

**Pontos de Acesso:**
- Frontend: http://localhost:4200
- API Backend: http://localhost:8000
- Documentação API: http://localhost:8000/docs
- Banco de dados: localhost:5432 (dev_user / dev_password)

### Parar os Serviços

```bash
docker-compose down

# Remover todos os dados
docker-compose down -v
```

## Desenvolvimento

### Visualizar Logs
```bash
docker-compose logs -f                # Todos os serviços
docker-compose logs -f backend        # Apenas backend
docker-compose logs -f frontend       # Apenas frontend
docker-compose logs -f db             # Apenas banco de dados
```

### Acessar Containers
```bash
docker-compose exec backend bash      # Shell do backend
docker-compose exec frontend bash     # Shell do frontend
docker-compose exec db psql -U dev_user -d app_db  # Shell do banco de dados
```

### Executar Testes
```bash
docker-compose exec -T backend python -m pytest
```

## Arquitetura

- **Frontend**: Angular 21 standalone (porta 4200)
- **Backend**: FastAPI async (porta 8000)  
- **Banco de dados**: PostgreSQL 15 + PostGIS (porta 5432)

Todos os serviços se comunicam através da rede Docker `medtime-network`.

## Configuração

Variáveis de ambiente padrão (em `docker-compose.yml`):
- `POSTGRES_USER`: dev_user
- `POSTGRES_PASSWORD`: dev_password
- `POSTGRES_DB`: app_db
- `DATABASE_URL`: postgresql+asyncpg://dev_user:dev_password@db:5432/app_db

## Solução de Problemas

**Porta já em uso:**
```bash
docker-compose down -v
docker-compose up -d
```

**Containers não iniciam:**
```bash
docker-compose logs          # Verificar logs
docker ps -a                # Ver todos os containers
```

**Conexão com banco de dados falha:**
O banco de dados leva ~15 segundos para inicializar. Aguarde e tente conectar novamente.

## Para Deployment no AWS

A aplicação está containerizada e pronta para deploy no AWS:
- Todos os serviços estão definidos em `docker-compose.yml`
- Use AWS ECS, EKS ou Fargate com os Dockerfiles fornecidos
- Atualize as variáveis de ambiente para produção:
  - `DATABASE_URL` - use endpoint do RDS
  - URL da API do Frontend - aponte para backend em produção
  - Ative HTTPS/TLS

## Estrutura do Projeto

```
.
├── backend/              # Aplicação FastAPI
├── frontend/             # Aplicação Angular
├── alembic/              # Migrações do banco de dados
├── Dockerfile.backend    # Container do backend
├── frontend/Dockerfile   # Container do frontend
├── docker-compose.yml    # Setup local
└── README.md            # Este arquivo
```

## Documentação

- Backend: [UC001](docs/UC001.md), [UC004](docs/UC004.md), [UC008](docs/UC008.md)
- Arquitetura: [docs/arquitetura.md](docs/arquitetura.md)
- Requisitos: [docs/Lista_Requisitos.md](docs/Lista_Requisitos.md)

