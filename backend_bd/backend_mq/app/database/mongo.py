# app/database/mongo.py

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from bson.objectid import ObjectId
from typing import Dict, List
import os
import logging

# Logger
logger = logging.getLogger(__name__)

# Conexão MongoDB
try:
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
    if not MONGODB_URI or not MONGODB_DATABASE:
        raise ValueError("Variáveis de ambiente MONGODB_URI ou MONGODB_DATABASE não definidas.")

    client = MongoClient(MONGODB_URI)
    db: Database = client[MONGODB_DATABASE]
    collection_interacoes: Collection = db["interacoes"]

except Exception as e:
    logger.error(f"Erro ao conectar ao MongoDB: {e}")
    raise RuntimeError("Falha na configuração do MongoDB")

# -----------------------------------------------------------------------------
# Função para salvar uma interação no MongoDB
# -----------------------------------------------------------------------------

def salvar_interacao(interacao_dict: Dict) -> str:
    """
    Persiste a interação no MongoDB e retorna o ID do documento.
    """
    try:
        resultado = collection_interacoes.insert_one(interacao_dict)
        return str(resultado.inserted_id)
    except Exception as e:
        logger.error(f"Erro ao salvar interação no MongoDB: {e}")
        raise RuntimeError("Erro ao salvar interação no banco de dados")

# -----------------------------------------------------------------------------
# Função para recuperar o histórico de um usuário
# -----------------------------------------------------------------------------

def buscar_historico_por_usuario(user_id: str) -> List[Dict]:
    """
    Recupera todas as interações de um usuário, ordenadas por timestamp.
    """
    try:
        documentos = list(
            collection_interacoes.find({"user_id": user_id}).sort("timestamp", 1)
        )
        return documentos
    except Exception as e:
        logger.error(f"Erro ao buscar histórico para user_id={user_id}: {e}")
        raise RuntimeError("Erro ao buscar histórico no banco de dados")

