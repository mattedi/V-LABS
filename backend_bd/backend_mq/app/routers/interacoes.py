from fastapi import APIRouter, HTTPException, Query
from app.schemas import InteractionCreate
#from app.database.mongo import salvar_interacao, obter_interacoes
from app.database.qdrant_client import indexar_documento
from sentence_transformers import SentenceTransformer
from datetime import datetime
import logging
from typing import List, Dict

router = APIRouter(prefix="/interacoes", tags=["interacoes"])

# Modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Nome da coleção no Qdrant
collection_name = "interacoes"

# Logger
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# POST /interacoes/ — Criar uma nova interação
# -----------------------------------------------------------------------------

@router.post("/", summary="Criar uma nova interação")
def criar_interacao(interacao: InteractionCreate):
    try:
        logger.info(f"Recebendo interação: {interacao.json()}")

        # 1. Persistência no MongoDB
        logger.info("Salvando interação no MongoDB...")
        mongo_id = salvar_interacao({
            "user_id": interacao.user_id,
            "pergunta": interacao.pergunta,
            "resposta": interacao.resposta,
            "complexidade": interacao.complexidade,
            "analise": {
                "pontos_fortes": interacao.analise.pontos_fortes,
                "aspectos_melhorar": interacao.analise.aspectos_melhorar,
                "passos_recomendados": interacao.analise.passos_recomendados,
            },
            "timestamp": interacao.timestamp.isoformat()
        })
        logger.info(f"Interação salva com ID: {mongo_id}")

        # 2. Vetorização
        logger.info("Vetorizando pergunta para Qdrant...")
        vetor = model.encode(interacao.pergunta).tolist()

        # 3. Indexação no Qdrant
        logger.info("Indexando no Qdrant...")
        payload = {
            "user_id": interacao.user_id,
            "pergunta": interacao.pergunta,
            "resposta": interacao.resposta,
            "timestamp": interacao.timestamp.isoformat()
        }
        indexar_documento(collection_name, mongo_id, vetor, payload)

        logger.info("Interação processada com sucesso.")
        return {"message": "Interação salva com sucesso", "id": mongo_id}

    except Exception as e:
        logger.exception("Erro ao criar interação")  # ← imprime traceback
        raise HTTPException(status_code=500, detail="Erro ao salvar interação")



# -----------------------------------------------------------------------------
# GET /interacoes/ — Listar interações por user_id
# -----------------------------------------------------------------------------

@router.get("/", summary="Listar interações por usuário")
def listar_interacoes(user_id: str = Query(...)) -> List[Dict]:
    """
    Retorna todas as interações salvas para um determinado usuário.
    """
    try:
        interacoes = obter_interacoes(user_id)
        mensagens = []

        for doc in interacoes:
            timestamp = doc.get("timestamp", datetime.utcnow())
            if isinstance(timestamp, str):
                try:
                    timestamp = datetime.fromisoformat(timestamp)
                except Exception:
                    timestamp = datetime.utcnow()

            mensagens.extend([
                {
                    "id": str(doc["_id"]) + "-user",
                    "text": doc.get("pergunta", ""),
                    "sender": "user",
                    "timestamp": timestamp,
                },
                {
                    "id": str(doc["_id"]) + "-assistant",
                    "text": doc.get("resposta", ""),
                    "sender": "assistant",
                    "timestamp": timestamp,
                },
            ])

        mensagens.sort(key=lambda m: m["timestamp"])
        return mensagens

    except Exception as e:
        logger.error(f"Erro ao listar interações para user_id={user_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro ao recuperar histórico de interações")


