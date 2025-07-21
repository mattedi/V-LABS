from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from bson import ObjectId
from app.database.mongo import colecao_respostas
from app.database.qdrant_client import indexar_documento

from app.services.embedding_service import gerar_vetor

router = APIRouter()

class Resposta(BaseModel):
    texto: str
    pergunta_id: str

class RespostaOut(Resposta):
    id: str

@router.get("/respostas/ping")
def ping():
    return {"mensagem": "Ping Respostas"}

@router.get("/respostas", response_model=List[RespostaOut])
def listar():
    respostas = colecao_respostas.find()
    return [
        {
            "id": str(r["_id"]),
            "texto": r["texto"],
            "pergunta_id": r["pergunta_id"]
        }
        for r in respostas
    ]

@router.post("/respostas", response_model=RespostaOut)
def criar(resposta: Resposta):
    try:
        # Inserir no MongoDB
        result = colecao_respostas.insert_one(resposta.dict())
        resposta_id = str(result.inserted_id)
        
        # Gerar vetor e indexar no Qdrant
        vetor = gerar_vetor(resposta.texto)
        payload = {**resposta.dict(), "id": resposta_id}
        indexar_documento("respostas", resposta_id, vetor, payload)
        
        return {**resposta.dict(), "id": resposta_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar resposta: {str(e)}")

@router.put("/respostas/{resposta_id}")
def atualizar(resposta_id: str, resposta: Resposta):
    try:
        result = colecao_respostas.update_one(
            {"_id": ObjectId(resposta_id)},
            {"$set": resposta.dict()}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Resposta não encontrada")
            
        # Atualizar índice no Qdrant
        vetor = gerar_vetor(resposta.texto)
        payload = {**resposta.dict(), "id": resposta_id}
        indexar_documento("respostas", resposta_id, vetor, payload)
        
        return {"mensagem": "Resposta atualizada"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar: {str(e)}")

@router.delete("/respostas/{resposta_id}")
def deletar(resposta_id: str):
    result = colecao_respostas.delete_one({"_id": ObjectId(resposta_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    return {"mensagem": "Resposta deletada"}
