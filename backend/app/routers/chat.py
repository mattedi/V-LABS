# backend_com/app/routers/chat.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../backend_bd')))


from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime

from backend_bd.backend_mq.app.models.interaction import InteractionCreate
from backend_bd.backend_mq.app.database.mongo import salvar_interacao
from backend_bd.backend_mq.app.services.embedding_service import gerar_embedding
from backend_bd.backend_mq.app.services.qdrant_service import salvar_no_qdrant
from backend_bd.backend_mq.app.database.mongo import buscar_historico_por_usuario



router = APIRouter()

@router.post("/chat/pergunta")
def registrar_pergunta(interacao: InteractionCreate):
    doc = interacao.dict()
    doc["timestamp"] = interacao.timestamp.isoformat()

    # Persistência em MongoDB
    mongo_id = salvar_interacao(doc)

    # Embedding da pergunta
    vetor = gerar_embedding(interacao.pergunta)

    # Persistência em Qdrant
    salvar_no_qdrant(
        user_id=interacao.user_id,
        texto=interacao.pergunta,
        resposta=interacao.resposta,
        vetor=vetor,
        timestamp=interacao.timestamp.isoformat()
    )

    return {"status": "ok", "mongo_id": mongo_id}


@router.get("/chat/historico", response_model=List[InteractionCreate])
def obter_historico(user_id: str = Query(..., description="ID do usuário para busca do histórico")):
    try:
        historico = buscar_historico_por_usuario(user_id)
        return historico
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar histórico: {str(e)}")


