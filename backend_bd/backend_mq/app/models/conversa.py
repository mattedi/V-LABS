from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MensagemModel(BaseModel):
    tipo: str  # "usuario" ou "assistente"
    conteudo: str
    timestamp: datetime
    complexidade: Optional[int] = None
    feedback: Optional[str] = None

class ConversaModel(BaseModel):
    id: Optional[str] = None
    titulo: str
    mensagens: List[MensagemModel] = []
    data_criacao: datetime
    data_ultima_interacao: datetime
    usuario_id: Optional[str] = None