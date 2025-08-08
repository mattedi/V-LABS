from fastapi import APIRouter, HTTPException
from app.models.conversa import ConversaModel, MensagemModel
from app.database.mongo import colecao_conversas
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/conversas", response_model=ConversaModel)
async def criar_conversa(conversa: ConversaModel):
    """Cria nova conversa."""
    conversa_dict = conversa.dict()
    conversa_dict["data_criacao"] = datetime.now()
    conversa_dict["data_ultima_interacao"] = datetime.now()
    
    resultado = colecao_conversas.insert_one(conversa_dict)
    conversa_dict["id"] = str(resultado.inserted_id)
    return ConversaModel(**conversa_dict)

@router.get("/conversas/{conversa_id}")
async def obter_conversa(conversa_id: str):
    """Obtém conversa por ID."""
    conversa = colecao_conversas.find_one({"_id": ObjectId(conversa_id)})
    if not conversa:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    conversa["id"] = str(conversa["_id"])
    del conversa["_id"]
    return conversa

@router.post("/conversas/{conversa_id}/mensagens")
async def adicionar_mensagem(conversa_id: str, mensagem: MensagemModel):
    """Adiciona mensagem à conversa."""
    mensagem_dict = mensagem.dict()
    mensagem_dict["timestamp"] = datetime.now()
    
    resultado = colecao_conversas.update_one(
        {"_id": ObjectId(conversa_id)},
        {
            "$push": {"mensagens": mensagem_dict},
            "$set": {"data_ultima_interacao": datetime.now()}
        }
    )
    
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    return {"status": "mensagem adicionada"}

@router.get("/conversas")
async def listar_conversas(limite: int = 50):
    """Lista todas as conversas."""
    conversas = list(colecao_conversas.find().sort("data_ultima_interacao", -1).limit(limite))
    
    for conversa in conversas:
        conversa["id"] = str(conversa["_id"])
        del conversa["_id"]
    
    return conversas