from sqlalchemy import Column, Integer, String, Float
from db import Base


class Aluno(Base):
    __tablename__ = 'alunos'
    id = Column(Integer, primary_key=True)
    matricula = Column(Integer)
    nome = Column(String(256))
    cr = Column(Float)
    idade = Column(Integer)
