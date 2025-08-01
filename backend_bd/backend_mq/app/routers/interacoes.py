from fastapi import APIRouter, HTTPException
from app.schemas import InteractionCreate
from app.database.mongo import salvar_interacao
from app.database.qdrant_client import indexar_documento
from sentence_transformers import SentenceTransformer
import logging

router = APIRouter(prefix="/interacoes", tags=["interacoes"])

model = SentenceTransformer("all-MiniLM-L6-v2")
collection_name = "interacoes"

logger = logging.getLogger(__name__)

@router.post("/")
def criar_interacao(interacao: InteractionCreate):
    try:
        # 1. Salvar no MongoDB
        mongo_id = salvar_interacao(interacao.dict())

        # 2. Gerar vetor da pergunta
        vetor = model.encode(interacao.pergunta).tolist()

        # 3. Indexar no Qdrant
        payload = {
            "user_id": interacao.user_id,
            "pergunta": interacao.pergunta,
            "resposta": interacao.resposta,
            "timestamp": interacao.timestamp.isoformat()
        }
        indexar_documento(collection_name, mongo_id, vetor, payload)

        return {"message": "Interação salva com sucesso", "id": mongo_id}
    except Exception as e:
        logger.error(f"Erro ao criar interação: {e}")
        raise HTTPException(status_code=500, detail="Erro ao salvar interação")
