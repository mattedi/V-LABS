from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class AnalisePergunta(BaseModel):
    pontos_fortes: List[str]
    aspectos_melhorar: List[str]
    passos_recomendados: List[str]

class InteractionCreate(BaseModel):
    user_id: str
    pergunta: str
    resposta: str
    complexidade: float
    analise: AnalisePergunta
    timestamp: datetime = Field(default_factory=datetime.utcnow)

