# app/routers/perguntas.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from app.services.embedding_service import gerar_vetor
from app.database.qdrant import indexar_documento

router = APIRouter()

class Pergunta(BaseModel):
    id: Optional[int]
    texto: str
    categoria: Optional[str] = None

perguntas_db: List[Pergunta] = []

@router.get("/perguntas/similar")
def buscar_similares(texto: str, limite: int = 5):
    from app.database.qdrant import buscar_por_texto
    resultados = buscar_por_texto("perguntas", texto, limite)
    return resultados


@router.get("/perguntas/ping")
def ping():
    return {"mensagem": "Ping Perguntas"}

@router.get("/perguntas")
def listar():
    return perguntas_db

@router.post("/perguntas")
def criar(pergunta: Pergunta):
    perguntas_db.append(pergunta)
    if pergunta.texto:
        vetor = gerar_vetor(pergunta.texto)
        payload = pergunta.dict()
        indexar_documento("perguntas", str(pergunta.id or len(perguntas_db)), vetor, payload)
    return pergunta

@router.put("/perguntas/{pergunta_id}")
def atualizar(pergunta_id: int, pergunta: Pergunta):
    for i, p in enumerate(perguntas_db):
        if p.id == pergunta_id:
            perguntas_db[i] = pergunta
            return pergunta
    return {"erro": "Pergunta não encontrada"}

@router.delete("/perguntas/{pergunta_id}")
def deletar(pergunta_id: int):
    for i, p in enumerate(perguntas_db):
        if p.id == pergunta_id:
            del perguntas_db[i]
            return {"mensagem": "Pergunta deletada"}
    return {"erro": "Pergunta não encontrada"}