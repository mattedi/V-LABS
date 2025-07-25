"""
Modelos de requisição para o backend_com.

Define todos os esquemas Pydantic para dados de entrada via API.
"""

from typing import Optional, List, Dict, Any
from pydantic import Field, EmailStr, validator

from .base import (
    BaseModel,
    TipoMultimodalEnum,
    NivelDificuldadeEnum,
    TipoAvaliacaoEnum,
    MetadadosBase,
    ConfiguracaoIA,
)


class UsuarioRequest(BaseModel):
    """
    Modelo para criação/atualização de usuário.
    """
    
    nome: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nome completo do usuário"
    )
    email: EmailStr = Field(
        ...,
        description="Email válido do usuário"
    )
    senha: Optional[str] = Field(
        None,
        min_length=8,
        max_length=128,
        description="Senha do usuário (mínimo 8 caracteres)"
    )
    tipo_usuario: str = Field(
        default="student",
        description="Tipo de usuário (student, teacher, admin)"
    )
    instituicao: Optional[str] = Field(
        None,
        max_length=200,
        description="Instituição de ensino"
    )
    configuracoes: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Configurações personalizadas do usuário"
    )
    
    @validator('senha')
    def validar_senha(cls, v):
        if v is not None and len(v) < 8:
            raise ValueError('Senha deve ter pelo menos 8 caracteres')
        return v


class LoginRequest(BaseModel):
    """
    Modelo para autenticação de usuário.
    """
    
    email: EmailStr = Field(
        ...,
        description="Email do usuário"
    )
    senha: str = Field(
        ...,
        min_length=1,
        description="Senha do usuário"
    )
    lembrar_me: bool = Field(
        default=False,
        description="Manter sessão ativa por mais tempo"
    )


class PerguntaRequest(BaseModel):
    """
    Modelo para submissão de perguntas multimodais.
    """
    
    usuario_id: str = Field(
        ...,
        description="ID do usuário que fez a pergunta"
    )
    conteudo: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Conteúdo textual da pergunta"
    )
    tipo_entrada: TipoMultimodalEnum = Field(
        default=TipoMultimodalEnum.TEXT,
        description="Tipo de entrada multimodal"
    )
    arquivos_anexos: Optional[List[str]] = Field(
        default_factory=list,
        description="Lista de URLs ou IDs de arquivos anexados"
    )
    contexto: Optional[str] = Field(
        None,
        max_length=2000,
        description="Contexto adicional para a pergunta"
    )
    disciplina: Optional[str] = Field(
        None,
        max_length=100,
        description="Disciplina relacionada à pergunta"
    )
    nivel_dificuldade: Optional[NivelDificuldadeEnum] = Field(
        None,
        description="Nível de dificuldade esperado"
    )
    metadados: Optional[MetadadosBase] = Field(
        default_factory=MetadadosBase,
        description="Metadados adicionais"
    )
    config_ia: Optional[ConfiguracaoIA] = Field(
        default_factory=ConfiguracaoIA,
        description="Configurações específicas para IA"
    )


class RespostaRequest(BaseModel):
    """
    Modelo para submissão de respostas.
    """
    
    pergunta_id: str = Field(
        ...,
        description="ID da pergunta sendo respondida"
    )
    usuario_id: str = Field(
        ...,
        description="ID do usuário que está respondendo"
    )
    conteudo: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Conteúdo da resposta"
    )
    confianca: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Nível de confiança na resposta (0-1)"
    )
    tempo_resposta: Optional[int] = Field(
        None,
        ge=0,
        description="Tempo gasto para responder (em segundos)"
    )
    referencias: Optional[List[str]] = Field(
        default_factory=list,
        description="Lista de referências utilizadas"
    )
    metadados: Optional[MetadadosBase] = Field(
        default_factory=MetadadosBase,
        description="Metadados adicionais"
    )


class AvaliacaoRequest(BaseModel):
    """
    Modelo para avaliação de respostas.
    """
    
    resposta_id: str = Field(
        ...,
        description="ID da resposta sendo avaliada"
    )
    avaliador_id: str = Field(
        ...,
        description="ID do usuário que está avaliando"
    )
    nota: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="Nota atribuída (0-10)"
    )
    tipo_avaliacao: TipoAvaliacaoEnum = Field(
        default=TipoAvaliacaoEnum.FORMATIVA,
        description="Tipo de avaliação realizada"
    )
    feedback: Optional[str] = Field(
        None,
        max_length=2000,
        description="Feedback textual sobre a resposta"
    )
    criterios: Optional[Dict[str, float]] = Field(
        default_factory=dict,
        description="Critérios específicos de avaliação"
    )
    sugestoes_melhoria: Optional[List[str]] = Field(
        default_factory=list,
        description="Sugestões para melhoria"
    )
    metadados: Optional[MetadadosBase] = Field(
        default_factory=MetadadosBase,
        description="Metadados adicionais"
    )


class EmbeddingRequest(BaseModel):
    """
    Modelo para geração de embeddings.
    """
    
    texto: str = Field(
        ...,
        min_length=1,
        max_length=8000,
        description="Texto para gerar embedding"
    )
    modelo: Optional[str] = Field(
        default="text-embedding-ada-002",
        description="Modelo de embedding a ser usado"
    )
    usuario_id: Optional[str] = Field(
        None,
        description="ID do usuário (para auditoria)"
    )
    contexto: Optional[str] = Field(
        None,
        max_length=1000,
        description="Contexto adicional para o embedding"
    )
    metadados: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Metadados para indexação"
    )


class BuscaSemanticaRequest(BaseModel):
    """
    Modelo para busca semântica no Qdrant.
    """
    
    query: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Consulta para busca semântica"
    )
    limite: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Número máximo de resultados"
    )
    score_threshold: Optional[float] = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Score mínimo para considerar resultado relevante"
    )
    filtros: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Filtros adicionais para a busca"
    )
    usuario_id: Optional[str] = Field(
        None,
        description="ID do usuário (para personalização)"
    )