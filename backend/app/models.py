from sqlalchemy import Column, Integer, String, Float, Index
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

    # Delega o gerenciamento do índice ao SQLAlchemy/Alembic
    __table_args__ = (
        Index('idx_unidades_localizacao', 'localizacao', postgresql_using='gist'),
    )

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    sobrenome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)