from pydantic import BaseModel
from typing import List
from datetime import datetime
from typing import List, Union
from pydantic import BaseModel

class AnaliseInteracao(BaseModel):
    pontos_fortes: List[str]
    aspectos_melhorar: List[str]
    passos_recomendados: List[str]

class InteractionCreate(BaseModel):
    user_id: str
    pergunta: str
    resposta: str
    complexidade: float
    analise: AnaliseInteracao
    timestamp: datetime

class InteractionAnalysis(BaseModel):
    pontos_fortes: Union[str, List[str]]
    aspectos_melhorar: Union[str, List[str]]
    passos_recomendados: Union[str, List[str]]