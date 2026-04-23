import asyncio
import random
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.database import AsyncSessionLocal
from backend.app.models import Unidade, Paciente, Atendimento

async def upsert_unidades(session: AsyncSession):
    unidades_dados = [
        {"nome": "Hospital das Clínicas da FMUSP", "endereco": "Av. Dr. Enéas Carvalho de Aguiar, 255", "tempo_medio_minutos": 120.0, "localizacao": "SRID=4326;POINT(-46.6678 -23.5574)"},
        {"nome": "Santa Casa de Misericórdia de São Paulo", "endereco": "R. Dr. Cesário Mota Júnior, 112", "tempo_medio_minutos": 90.0, "localizacao": "SRID=4326;POINT(-46.6496 -23.5432)"},
        {"nome": "Hospital São Paulo", "endereco": "R. Napoleão de Barros, 715", "tempo_medio_minutos": 105.0, "localizacao": "SRID=4326;POINT(-46.6443 -23.5975)"},
        {"nome": "UPA Itaquera", "endereco": "Rua Píres do Rio, 134", "tempo_medio_minutos": 45.0, "localizacao": "SRID=4326;POINT(-46.4635 -23.5350)"},
        {"nome": "Hospital Municipal M'Boi Mirim", "endereco": "Estr. do M'Boi Mirim, 5203", "tempo_medio_minutos": 150.0, "localizacao": "SRID=4326;POINT(-46.7725 -23.6811)"},
        {"nome": "Hospital do Servidor Público Estadual", "endereco": "R. Pedro de Toledo, 1800", "tempo_medio_minutos": 60.0, "localizacao": "SRID=4326;POINT(-46.6548 -23.5955)"}
    ]
    
    unidades_objs = []
    for dado in unidades_dados:
        stmt = select(Unidade).where(Unidade.nome == dado["nome"])
        result = await session.execute(stmt)
        item = result.scalars().first()
        
        if item:
            for key, value in dado.items():
                setattr(item, key, value)
        else:
            item = Unidade(**dado)
            session.add(item)
        unidades_objs.append(item)
    
    await session.flush() # Garante IDs para os relacionamentos
    return unidades_objs

async def upsert_pacientes(session: AsyncSession):
    pacientes_dados = [
        {"nome": "Mateus", "sobrenome": "Teles Magalhães", "email": "mateus.magalhaes@mock.com"},
        {"nome": "João", "sobrenome": "Silva", "email": "joao.silva@mock.com"},
        {"nome": "Maria", "sobrenome": "Oliveira", "email": "maria.oliveira@mock.com"},
        {"nome": "Ana", "sobrenome": "Costa", "email": "ana.costa@mock.com"},
        {"nome": "Carlos", "sobrenome": "Pereira", "email": "carlos.p@mock.com"}
    ]
    
    pacientes_objs = []
    for dado in pacientes_dados:
        stmt = select(Paciente).where(Paciente.email == dado["email"])
        result = await session.execute(stmt)
        item = result.scalars().first()
        
        if item:
            for key, value in dado.items():
                setattr(item, key, value)
        else:
            item = Paciente(**dado)
            session.add(item)
        pacientes_objs.append(item)
        
    await session.flush()
    return pacientes_objs

async def gerar_atendimentos(session: AsyncSession, unidades, pacientes, quantidade=50):
    # Limpa atendimentos antigos para não duplicar massa de teste
    # Remova se preferir acumular dados
    atendimentos = []
    status_opcoes = ["Finalizado", "Em Atendimento", "Aguardando"]
    agora = datetime.now()

    for _ in range(quantidade):
        u = random.choice(unidades)
        p = random.choice(pacientes)
        
        # Simulação de tempos
        chegada = agora - timedelta(minutes=random.randint(60, 480))
        espera_triagem = random.randint(10, 40)
        triagem = chegada + timedelta(minutes=espera_triagem)
        
        # Nem todos foram atendidos ainda (para validar nulos)
        status = random.choice(status_opcoes)
        atendimento_medico = None
        
        if status == "Finalizado":
            espera_medico = random.randint(20, 120)
            atendimento_medico = triagem + timedelta(minutes=espera_medico)

        atendimentos.append(Atendimento(
            unidade_id=u.id,
            paciente_id=p.id,
            status=status,
            horario_chegada=chegada,
            horario_triagem=triagem,
            horario_atendimento=atendimento_medico
        ))
    
    session.add_all(atendimentos)

async def run_seed():
    async with AsyncSessionLocal() as session:
        print("Iniciando Upsert de Unidades e Pacientes...")
        unidades = await upsert_unidades(session)
        pacientes = await upsert_pacientes(session)
        
        print("Gerando massa de Atendimentos...")
        await gerar_atendimentos(session, unidades, pacientes)
        
        await session.commit()
        print("Seed concluída com sucesso.")

if __name__ == "__main__":
    asyncio.run(run_seed())