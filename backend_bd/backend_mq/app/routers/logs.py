# app/routers/logs.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from app.database.mongo import colecao_logs  # conexão à coleção "logs"

router = APIRouter()

# Modelo de entrada
class Log(BaseModel):
    acao: str
    timestamp: Optional[datetime] = datetime.utcnow()

class LogOut(Log):
    id: str

@router.get("/logs/ping")
def ping():
    return {"mensagem": "Ping Logs"}

@router.get("/logs", response_model=List[LogOut])
def listar():
    logs = colecao_logs.find()
    return [
        {"id": str(l["_id"]), "acao": l["acao"], "timestamp": l["timestamp"]}
        for l in logs
    ]

@router.post("/logs", response_model=LogOut)
def criar(log: Log):
    result = colecao_logs.insert_one(log.dict())
    return {**log.dict(), "id": str(result.inserted_id)}

@router.put("/logs/{log_id}")
def atualizar(log_id: str, log: Log):
    result = colecao_logs.update_one(
        {"_id": ObjectId(log_id)},
        {"$set": log.dict()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Log não encontrado")
    return {"mensagem": "Log atualizado"}

@router.delete("/logs/{log_id}")
def deletar(log_id: str):
    result = colecao_logs.delete_one({"_id": ObjectId(log_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Log não encontrado")
    return {"mensagem": "Log deletado"}
