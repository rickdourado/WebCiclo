from sqlalchemy import (
    Column, Integer, String, Text, Enum, DateTime, Date, Time, 
    DECIMAL, ForeignKey, TIMESTAMP, func
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    ativo = Column(Enum('sim', 'nao'), default='sim')
    ultimo_acesso = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

class Curso(Base):
    __tablename__ = 'cursos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_acao = Column(Enum('Curso', 'Oficina', 'Palestra', 'Workshop', 'Evento'), nullable=False)
    titulo = Column(String(255), nullable=False)
    titulo_original = Column(String(255), nullable=True)
    descricao = Column(Text, nullable=False)
    descricao_original = Column(Text, nullable=True)
    capa_curso = Column(String(500), nullable=True)
    inicio_inscricoes = Column(DateTime, nullable=False)
    fim_inscricoes = Column(DateTime, nullable=False)
    orgao = Column(String(255), nullable=False)
    tema = Column(String(100), nullable=False)
    carga_horaria = Column(String(100), nullable=False)
    modalidade = Column(Enum('Presencial', 'Online', 'Híbrido'), nullable=False)
    acessibilidade = Column(Enum('acessivel', 'exclusivo', 'nao_acessivel'), nullable=False)
    recursos_acessibilidade = Column(Text, nullable=True)
    publico_alvo = Column(Text, nullable=False)
    curso_gratuito = Column(Enum('sim', 'nao'), nullable=False, default='sim')
    valor_curso_inteira = Column(DECIMAL(10, 2), nullable=True)
    valor_curso_meia = Column(DECIMAL(10, 2), nullable=True)
    requisitos_meia = Column(Text, nullable=True)
    oferece_certificado = Column(Enum('sim', 'nao'), nullable=False)
    pre_requisitos = Column(Text, nullable=True)
    oferece_bolsa = Column(Enum('sim', 'nao'), nullable=False, default='nao')
    valor_bolsa = Column(DECIMAL(10, 2), nullable=True)
    requisitos_bolsa = Column(Text, nullable=True)
    info_complementares = Column(Text, nullable=True)
    info_adicionais = Column(Text, nullable=True)
    parceiro_externo = Column(Enum('sim', 'nao'), nullable=False, default='nao')
    parceiro_nome = Column(String(255), nullable=True)
    parceiro_link = Column(String(500), nullable=True)
    parceiro_logo = Column(String(500), nullable=True)
    csv_file = Column(String(500), nullable=True)
    pdf_file = Column(String(500), nullable=True)
    status = Column(Enum('ativo', 'inativo', 'rascunho'), default='ativo')
    is_inserted = Column(Enum('sim', 'nao'), default='nao')
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(Integer, nullable=True)

    # Relationships
    turmas = relationship("Turma", back_populates="curso", cascade="all, delete-orphan")
    plataformas_online = relationship("PlataformaOnline", back_populates="curso", cascade="all, delete-orphan")

class Turma(Base):
    __tablename__ = 'turmas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    curso_id = Column(Integer, ForeignKey('cursos.id', ondelete='CASCADE'), nullable=False)
    numero_turma = Column(Integer, nullable=False, default=1)
    nome_turma = Column(String(100), nullable=True)
    endereco_unidade = Column(String(500), nullable=True)
    bairro_unidade = Column(String(100), nullable=True)
    complemento = Column(String(255), nullable=True)
    vagas_totais = Column(Integer, nullable=False)
    vagas_ocupadas = Column(Integer, default=0)
    # Note: vagas_disponiveis is a detailed generated column in MySQL, SQLAlchemy doesn't manage generated columns perfectly in all versions without special syntax, 
    # but for migration generation, we can omit it if it's purely server-side or define it as Computed.
    # Alembic/SQLAlchemy support "Computed" columns.
    # vagas_disponiveis = Column(Integer, Computed("vagas_totais - vagas_ocupadas")) 
    # For now, I'll comment it out or leave it for Alembic to detect if it can? 
    # Generated columns are tricky. I'll omit it from the model for now to avoid complexity, or use FetchedValue.
    # Or actually, I should include it if I want autogenerate to not try to drop it.
    
    inicio_aulas = Column(Date, nullable=False)
    fim_aulas = Column(Date, nullable=False)
    horario_inicio = Column(Time, nullable=False)
    horario_fim = Column(Time, nullable=False)
    status = Column(Enum('ativa', 'inativa', 'cancelada', 'concluida'), default='ativa')
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    curso = relationship("Curso", back_populates="turmas")
    dias_semana = relationship("TurmaDiaSemana", back_populates="turma", cascade="all, delete-orphan")

class TurmaDiaSemana(Base):
    __tablename__ = 'turmas_dias_semana'

    id = Column(Integer, primary_key=True, autoincrement=True)
    turma_id = Column(Integer, ForeignKey('turmas.id', ondelete='CASCADE'), nullable=False)
    dia_semana = Column(Enum('Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'), nullable=False)

    turma = relationship("Turma", back_populates="dias_semana")

class PlataformaOnline(Base):
    __tablename__ = 'plataformas_online'

    id = Column(Integer, primary_key=True, autoincrement=True)
    curso_id = Column(Integer, ForeignKey('cursos.id', ondelete='CASCADE'), nullable=False)
    plataforma_digital = Column(String(255), nullable=False)
    link_acesso = Column(String(500), nullable=True)
    vagas_totais = Column(Integer, nullable=False)
    vagas_ocupadas = Column(Integer, default=0)
    # vagas_disponiveis generated column
    aulas_assincronas = Column(Enum('sim', 'nao'), nullable=False, default='sim')
    inicio_aulas = Column(Date, nullable=True)
    fim_aulas = Column(Date, nullable=True)
    horario_inicio = Column(Time, nullable=True)
    horario_fim = Column(Time, nullable=True)
    status = Column(Enum('ativa', 'inativa'), default='ativa')
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    curso = relationship("Curso", back_populates="plataformas_online")
