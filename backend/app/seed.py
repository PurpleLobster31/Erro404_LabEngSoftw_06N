import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Ajuste os imports conforme a estrutura real do seu projeto
from backend.app.database import AsyncSessionLocal
from backend.app.models import Unidade, Paciente

async def run_seed():
    async with AsyncSessionLocal() as session:
        # --- Carga de Unidades ---
        result_unidades = await session.execute(select(Unidade))
        if not result_unidades.scalars().first():
            unidades_mock = [
                Unidade(
                    nome="Hospital das Clínicas da FMUSP",
                    endereco="Av. Dr. Enéas Carvalho de Aguiar, 255 - Cerqueira César",
                    tempo_medio_minutos=120.0,
                    localizacao="SRID=4326;POINT(-46.6678 -23.5574)"  # Zona Oeste
                ),
                Unidade(
                    nome="Santa Casa de Misericórdia de São Paulo",
                    endereco="R. Dr. Cesário Mota Júnior, 112 - Vila Buarque",
                    tempo_medio_minutos=90.0,
                    localizacao="SRID=4326;POINT(-46.6496 -23.5432)"  # Centro
                ),
                Unidade(
                    nome="Hospital São Paulo",
                    endereco="R. Napoleão de Barros, 715 - Vila Clementino",
                    tempo_medio_minutos=105.0,
                    localizacao="SRID=4326;POINT(-46.6443 -23.5975)"  # Zona Sul
                ),
                Unidade(
                    nome="UPA Itaquera",
                    endereco="Rua Píres do Rio, 134 - Itaquera",
                    tempo_medio_minutos=45.0,
                    localizacao="SRID=4326;POINT(-46.4635 -23.5350)"  # Zona Leste
                ),
                Unidade(
                    nome="Hospital Municipal M'Boi Mirim",
                    endereco="Estr. do M'Boi Mirim, 5203 - Jardim Angela",
                    tempo_medio_minutos=150.0,
                    localizacao="SRID=4326;POINT(-46.7725 -23.6811)"  # Extremo Sul
                ),
                Unidade(
                    nome="Hospital do Servidor Público Estadual",
                    endereco="R. Pedro de Toledo, 1800 - Vila Clementino",
                    tempo_medio_minutos=60.0,
                    localizacao="SRID=4326;POINT(-46.6548 -23.5955)"  # Zona Sul / Ibirapuera
                )
            ]
            session.add_all(unidades_mock)
            print("Mock de Unidades (São Paulo) inserido.")

        # --- Carga de Pacientes ---
        result_pacientes = await session.execute(select(Paciente))
        if not result_pacientes.scalars().first():
            pacientes_mock = [
                Paciente(
                    nome="Mateus",
                    sobrenome="Teles Magalhães",
                    email="mateus.magalhaes@mock.com"
                ),
                Paciente(
                    nome="João",
                    sobrenome="Silva",
                    email="joao.silva@mock.com"
                ),
                Paciente(
                    nome="Maria",
                    sobrenome="Oliveira",
                    email="maria.oliveira@mock.com"
                )
            ]
            session.add_all(pacientes_mock)
            print("Mock de Pacientes inserido.")

        await session.commit()
        print("Carga de dados (Seed) concluída com sucesso.")

if __name__ == "__main__":
    asyncio.run(run_seed())