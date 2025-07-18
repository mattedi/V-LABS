# app/routers/logs.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()

class Log(BaseModel):
    id: Optional[int]
    acao: str
    timestamp: Optional[datetime] = datetime.utcnow()

logs_db: List[Log] = []

@router.get("/logs/ping")
def ping():
    return {"mensagem": "Ping Logs"}

@router.get("/logs")
def listar():
    return logs_db

@router.post("/logs")
def criar(log: Log):
    logs_db.append(log)
    return log

@router.put("/logs/{log_id}")
def atualizar(log_id: int, log: Log):
    for i, l in enumerate(logs_db):
        if l.id == log_id:
            logs_db[i] = log
            return log
    return {"erro": "Log não encontrado"}

@router.delete("/logs/{log_id}")
def deletar(log_id: int):
    for i, l in enumerate(logs_db):
        if l.id == log_id:
            del logs_db[i]
            return {"mensagem": "Log deletado"}
    return {"erro": "Log não encontrado"}
