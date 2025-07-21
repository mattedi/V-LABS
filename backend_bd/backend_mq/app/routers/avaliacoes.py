# app/routers/avaliacoes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from bson import ObjectId
from app.database.mongo import colecao_avaliacoes  # conexão à coleção "avaliacoes"

router = APIRouter()

# Modelos de entrada e saída
class Avaliacao(BaseModel):
    usuario_id: int
    pergunta_id: int
    nota: float

class AvaliacaoOut(Avaliacao):
    id: str

@router.get("/avaliacoes/ping")
def ping():
    return {"mensagem": "Ping Avaliacoes"}

@router.get("/avaliacoes", response_model=List[AvaliacaoOut])
def listar():
    avaliacoes = colecao_avaliacoes.find()
    return [
        {
            "id": str(a["_id"]),
            "usuario_id": a["usuario_id"],
            "pergunta_id": a["pergunta_id"],
            "nota": a["nota"]
        }
        for a in avaliacoes
    ]

@router.post("/avaliacoes", response_model=AvaliacaoOut)
def criar(avaliacao: Avaliacao):
    result = colecao_avaliacoes.insert_one(avaliacao.dict())
    return {**avaliacao.dict(), "id": str(result.inserted_id)}

@router.put("/avaliacoes/{avaliacao_id}")
def atualizar(avaliacao_id: str, avaliacao: Avaliacao):
    result = colecao_avaliacoes.update_one(
        {"_id": ObjectId(avaliacao_id)},
        {"$set": avaliacao.dict()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return {"mensagem": "Avaliação atualizada"}

@router.delete("/avaliacoes/{avaliacao_id}")
def deletar(avaliacao_id: str):
    result = colecao_avaliacoes.delete_one({"_id": ObjectId(avaliacao_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return {"mensagem": "Avaliação deletada"}
