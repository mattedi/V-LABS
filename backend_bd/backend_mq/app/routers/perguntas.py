from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from bson import ObjectId
from app.database.mongo import colecao_perguntas
from app.database.qdrant_client import indexar_documento, buscar_por_texto

from app.services.embedding_service import gerar_vetor

router = APIRouter()

class Pergunta(BaseModel):
    texto: str
    categoria: Optional[str] = None

class PerguntaOut(Pergunta):
    id: str

@router.get("/perguntas/ping")
def ping():
    return {"mensagem": "Ping Perguntas"}

@router.get("/perguntas", response_model=List[PerguntaOut])
def listar():
    perguntas = colecao_perguntas.find()
    return [
        {
            "id": str(p["_id"]),
            "texto": p["texto"],
            "categoria": p.get("categoria")
        }
        for p in perguntas
    ]

@router.post("/perguntas", response_model=PerguntaOut)
def criar(pergunta: Pergunta):
    try:
        # Inserir no MongoDB
        result = colecao_perguntas.insert_one(pergunta.dict())
        pergunta_id = str(result.inserted_id)
        
        # Gerar vetor e indexar no Qdrant
        vetor = gerar_vetor(pergunta.texto)
        payload = {**pergunta.dict(), "id": pergunta_id}
        indexar_documento("perguntas", pergunta_id, vetor, payload)
        
        return {**pergunta.dict(), "id": pergunta_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar pergunta: {str(e)}")

@router.get("/perguntas/similar")
def buscar_similares(texto: str, limite: int = 5):
    try:
        vetor = gerar_vetor(texto)
        resultados = buscar_por_texto("perguntas", vetor, limite)
        return {"resultados": resultados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")

@router.put("/perguntas/{pergunta_id}")
def atualizar(pergunta_id: str, pergunta: Pergunta):
    try:
        result = colecao_perguntas.update_one(
            {"_id": ObjectId(pergunta_id)},
            {"$set": pergunta.dict()}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Pergunta não encontrada")
            
        # Atualizar índice no Qdrant
        vetor = gerar_vetor(pergunta.texto)
        payload = {**pergunta.dict(), "id": pergunta_id}
        #indexar_documento("perguntas", pergunta_id, vetor, payload)
        
        return {"mensagem": "Pergunta atualizada"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar: {str(e)}")

@router.delete("/perguntas/{pergunta_id}")
def deletar(pergunta_id: str):
    result = colecao_perguntas.delete_one({"_id": ObjectId(pergunta_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    return {"mensagem": "Pergunta deletada"}
