# Guia de Configuração do Ambiente de Desenvolvimento

Este guia descreve os passos necessários para configurar e executar o ecossistema da API, incluindo o banco de dados geoespacial (PostGIS) e a camada de persistência assíncrona.

## 1. Pré-requisitos

É obrigatório ter as seguintes ferramentas instaladas:

* **Docker & Docker Compose**: Para orquestração do banco de dados.
* **Python 3.13+**: Versão base da aplicação.
* **Git**: Para versionamento.

## 2. Instalação Local

1.  **Ambiente Virtual**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    source venv/bin/activate # Linux/Mac
    ```

2.  **Dependências**:
    ```bash
    pip install -r requirements.txt
    pip install "pydantic[email]"
    ```

3.  **Variáveis de Ambiente**:
    Copie o arquivo `.env.example` para um novo arquivo `.env` na raiz do projeto:
    ```bash
    cp .env.example .env
    ```

## 3. Infraestrutura (Docker)

O banco de dados utiliza a imagem `postgis/postgis`, que já contém as extensões espaciais necessárias.

1.  **Subir o container**:
    ```bash
    docker-compose up -d
    ```
2.  **Tempo de Inicialização**: Após o container constar como "Running", o PostGIS executa scripts internos de configuração de topologia. **Aguarde 15 segundos** antes de prosseguir para as migrações, caso contrário, a conexão será recusada.

## 4. Persistência e Migrações (Alembic)

O projeto está configurado para lidar com as tabelas nativas do PostGIS e evitar a criação duplicada de índices espaciais.

1.  **Aplicar Esquema**:
    ```bash
    alembic upgrade head
    ```
    * **Nota Técnica**: O arquivo `alembic/env.py` contém uma função `custom_include_object` que ignora tabelas do *Tiger Geocoder* (ex: `addr`, `county`). Não remova esta configuração.

2.  **Popular o Banco (Seed)**:
    Execute o script para inserir unidades de saúde reais de São Paulo e pacientes de teste:
    ```bash
    python -m backend.app.seed
    ```

## 5. Execução da API

Inicie o servidor via Uvicorn a partir da raiz do projeto:

```bash
uvicorn backend.app.main:app --reload
```

* **Endpoint principal:** ```http://localhost:8000```
* **Documentação (Swagger):** ```http://localhost:8000/docs```

## Observação para desenvolvimento
### Adição de colunas especiais
Ao adicionar novas colunas do tipo Geometry no arquivo models.py, siga este padrão para evitar erros de colisão no Alembic:

1.  Defina ```spatial_index=False``` no campo ```Geometry```.
2.  Declare o índice explicitamente em ```__table_args__```.

Exemplo:
```python
localizacao = Column(Geometry(geometry_type='POINT', srid=4326, spatial_index=False))

__table_args__ = (
    Index('idx_unidades_localizacao', 'localizacao', postgresql_using='gist'),
)
```
### Consultas Espaciais (ST_Distance)
Para cálculos de distância em metros (raio de busca), utilize sempre o cast para Geography:

Exemplo:
```python
distancia = func.ST_Distance(
    func.cast(Unidade.localizacao, Geography),
    func.cast(ponto_referencia, Geography)
)
```
### Reset Completo do Ambiente
Caso o banco de dados fique inconsistente com as migrações locais:

1. ```docker-compose down -v``` (O parâmetro ```-v``` remove os volumes persistidos).

2. Apague os arquivos em ```alembic/versions/``` (se desejar reiniciar o histórico).

3. ```docker-compose up -d``` e siga novamente os passos de ```upgrade head``` e ```seed```.
