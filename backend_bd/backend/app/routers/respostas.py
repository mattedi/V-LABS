# app/routers/respostas.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from app.services.embedding_service import gerar_vetor
from app.database.qdrant import indexar_documento

router = APIRouter()

class Resposta(BaseModel):
    id: Optional[int]
    texto: str
    pergunta_id: Optional[int]

respostas_db: List[Resposta] = []

@router.get("/respostas/ping")
def ping():
    return {"mensagem": "Ping Respostas"}

@router.get("/respostas")
def listar():
    return respostas_db

@router.post("/respostas")
def criar(resposta: Resposta):
    respostas_db.append(resposta)
    if resposta.texto:
        vetor = gerar_vetor(resposta.texto)
        payload = resposta.dict()
        indexar_documento("respostas", str(resposta.id or len(respostas_db)), vetor, payload)
    return resposta

@router.put("/respostas/{resposta_id}")
def atualizar(resposta_id: int, resposta: Resposta):
    for i, r in enumerate(respostas_db):
        if r.id == resposta_id:
            respostas_db[i] = resposta
            return resposta
    return {"erro": "Resposta não encontrada"}

@router.delete("/respostas/{resposta_id}")
def deletar(resposta_id: int):
    for i, r in enumerate(respostas_db):
        if r.id == resposta_id:
            del respostas_db[i]
            return {"mensagem": "Resposta deletada"}
    return {"erro": "Resposta não encontrada"}
