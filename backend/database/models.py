from datetime import date, datetime
from typing import Any

from sqlalchemy import Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry

from backend.database.database import Base

class Unidade(Base):
    __tablename__ = "unidades"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(index=True)
    tipo: Mapped[str] = mapped_column()  # Ex: Hospital, UPA, UBS
    
    # Endereço Detalhado
    endereco: Mapped[str] = mapped_column()
    numero: Mapped[str | None] = mapped_column()
    complemento: Mapped[str | None] = mapped_column()
    cep: Mapped[str | None] = mapped_column()
    cidade: Mapped[str] = mapped_column()
    estado: Mapped[str] = mapped_column()
    
    # Contato
    telefone1: Mapped[str] = mapped_column()
    telefone2: Mapped[str | None] = mapped_column()
    
    # Metadados e Operação
    descricao: Mapped[str | None] = mapped_column()
    horario_funcionamento: Mapped[str | None] = mapped_column()
    
    # Geoespacial (PostGIS)
    localizacao: Mapped[Geometry] = mapped_column(
        Geometry(geometry_type='POINT', srid=4326),
        nullable=False
    )
    __table_args__ = (
        Index('idx_unidades_localizacao', 'localizacao', postgresql_using='gist'),
    )

    # Lado "Um" do relacionamento (Uma unidade tem muitos atendimentos)
    atendimentos: Mapped[list["Atendimento"]] = relationship(back_populates="unidade")


class Paciente(Base):
    __tablename__ = "pacientes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column()
    sobrenome: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True, index=True)
    data_nascimento: Mapped[date | None] = mapped_column()

    # Relacionamentos
    # Lado "Um" do relacionamento
    atendimentos: Mapped[list["Atendimento"]] = relationship(back_populates="paciente")


class Atendimento(Base):
    __tablename__ = "atendimentos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    unidade_id: Mapped[int] = mapped_column(ForeignKey("unidades.id"))
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"))
    status: Mapped[str] = mapped_column()
    horario_chegada: Mapped[datetime | None] = mapped_column()
    horario_triagem: Mapped[datetime | None] = mapped_column()
    horario_atendimento: Mapped[datetime | None] = mapped_column()

    # relacionamentos
    # Lado "Muitos" do relacionamento (Muitos atendimentos pertencem a uma unidade)
    unidade: Mapped["Unidade"] = relationship(back_populates="atendimentos")
    paciente: Mapped["Paciente"] = relationship(back_populates="atendimentos")