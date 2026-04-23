from sqlalchemy import Column, Integer, String, Float, Index, LargeBinary, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from backend.app.database import Base

class Unidade(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    endereco = Column(String, nullable=False)
    tempo_medio_minutos = Column(Float, nullable=True)
    
    # spatial_index=False impede a criação duplicada oculta
    localizacao = Column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=False), 
        nullable=True
    )

    imagem = Column(LargeBinary, nullable=True)
    # Delega o gerenciamento do índice ao SQLAlchemy/Alembic
    __table_args__ = (
        Index('idx_unidades_localizacao', 'localizacao', postgresql_using='gist'),
    )

    # Relacionamentos

    # Lado "Um" do relacionamento (Uma unidade tem muitos atendimentos)
    atendimentos = relationship("Atendimento", back_populates="unidade")

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    sobrenome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    data_nascimento = Column(Date, nullable=True)

    # Relacionamentos
    # Lado "Um" do relacionamento
    atendimentos = relationship("Atendimento", back_populates="paciente")
    

class Atendimento(Base):
    __tablename__ = "atendimentos"

    id = Column(Integer, primary_key=True, index=True)
    # nullable=False garante a obrigatoriedade no banco
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    status = Column(String, nullable=False)
    horario_chegada = Column(DateTime, nullable=True)
    horario_triagem = Column(DateTime, nullable=True)
    horario_atendimento = Column(DateTime, nullable=True)

    # relacionamentos
    # Lado "Muitos" do relacionamento (Muitos atendimentos pertencem a uma unidade)
    unidade = relationship("Unidade", back_populates="atendimentos")
    paciente = relationship("Paciente", back_populates="atendimentos")