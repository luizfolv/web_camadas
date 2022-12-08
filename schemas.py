from pydantic import BaseModel


class Aluno(BaseModel):
    matricula: int
    nome: str
    cr: float
    idade: int

