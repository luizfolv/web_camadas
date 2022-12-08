from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine
from sqlalchemy.orm import Session
import models
import schemas


Base.metadata.create_all(engine)

description = """
Desenvolvimento Web em Camadas 🚀

## Alunos API

Você pode consultar itens, inserir, atualizar e deletar.

## Participantes


* Luiz Felipe Oliveira Gonçalves Leitão - luiz.leitao@soulasalle.com.br
* João Marcos Salomão do Nascimento - joao.marcos@soulasalle.com.br
"""

app = FastAPI(docs_url="/api/docs", title="Aluno - WebCamadas",  description=description)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return "Desenvolvimento Web camadas.\nAlunos: Luiz Felipe, João Marcos"


@app.get("/aluno")
def read_aluno_list():
    session = Session(bind=engine, expire_on_commit=False)
    aluno_list = session.query(models.Aluno).all()

    session.close()

    return aluno_list

@app.get("/aluno/{id}")
def read_aluno(id: int):
    session = Session(bind=engine, expire_on_commit=False)
    aluno = session.query(models.Aluno).get(id)
    
    session.close()

    if not aluno:
        raise HTTPException(status_code=404, detail=f"O aluno com o id {id} não foi encontrado.")

    return aluno

@app.post("/aluno", status_code=status.HTTP_201_CREATED)
def create_aluno(aluno: schemas.Aluno):
    session = Session(bind=engine, expire_on_commit=False)
    alunodb = models.Aluno(matricula=aluno.matricula, nome=aluno.nome, cr=aluno.cr, idade=aluno.idade)    
    session.add(alunodb)
    session.commit()
    id = alunodb.id
    
    session.close()
    return f"Criado aluno com id {id}"


@app.put("/aluno/{id}")
def update_aluno(id: int, matricula: int, nome: str, cr: float, idade: int):
    session = Session(bind=engine, expire_on_commit=False)
    aluno = session.query(models.Aluno).get(id)

    if aluno:
        aluno.matricula = matricula
        aluno.nome = nome
        aluno.cr = cr
        aluno.idade = idade
        session.commit()

    session.close()

    if not aluno:
        raise HTTPException(status_code=404, detail=f"O aluno com id {id} não foi encontrado")

    return aluno

@app.delete("/aluno/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aluno(id: int):
    session = Session(bind=engine, expire_on_commit=False)
    aluno = session.query(models.Aluno).get(id)
    
    if aluno:
        session.delete(aluno)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"O aluno com o id {id} não foi encontrado")

    return None
