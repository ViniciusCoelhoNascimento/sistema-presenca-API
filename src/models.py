from sqlalchemy import (Boolean, Column, Integer, String, ForeignKey, 
    Text, DateTime)
from sqlalchemy.orm import relationship
import datetime
from database import Base

class Professores(Base):
    __tablename__ = "professores"
    id = Column(Integer, primary_key= True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Aulas(Base):
    __tablename__ = "aulas"
    id = Column(Integer, primary_key= True, index=True)
    descricao = Column(String)
    id_professor = Column(Integer, ForeignKey("professores.id"))

class Turmas(Base):
    __tablename__ = "turmas"
    id = Column(Integer, primary_key=True, index=True)
    nome_aluno = Column(String)
    presenca = Column(Boolean)
    id_aula = Column(Integer, ForeignKey("aulas.id"))
