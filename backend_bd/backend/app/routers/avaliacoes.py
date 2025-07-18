# app/routers/avaliacoes.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

class Avaliacao(BaseModel):
    id: Optional[int]
    usuario_id: int
    pergunta_id: int
    nota: float

avaliacoes_db: List[Avaliacao] = []

@router.get("/avaliacoes/ping")
def ping():
    return {"mensagem": "Ping Avaliacoes"}

@router.get("/avaliacoes")
def listar():
    return avaliacoes_db

@router.post("/avaliacoes")
def criar(avaliacao: Avaliacao):
    avaliacoes_db.append(avaliacao)
    return avaliacao

@router.put("/avaliacoes/{avaliacao_id}")
def atualizar(avaliacao_id: int, avaliacao: Avaliacao):
    for i, a in enumerate(avaliacoes_db):
        if a.id == avaliacao_id:
            avaliacoes_db[i] = avaliacao
            return avaliacao
    return {"erro": "Avaliacao não encontrada"}

@router.delete("/avaliacoes/{avaliacao_id}")
def deletar(avaliacao_id: int):
    for i, a in enumerate(avaliacoes_db):
        if a.id == avaliacao_id:
            del avaliacoes_db[i]
            return {"mensagem": "Avaliacao deletada"}
    return {"erro": "Avaliacao não encontrada"}
