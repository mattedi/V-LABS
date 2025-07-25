"""
Modelos de resposta para o backend_com.

Define todos os esquemas Pydantic para dados de saída via API.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Generic, TypeVar
from pydantic import Field

from .base import (
    BaseModel,
    TimestampedModel,
    StatusEnum,
    TipoMultimodalEnum,
    NivelDificuldadeEnum,
    TipoAvaliacaoEnum,
    MetadadosBase,
)

# TypeVar para respostas paginadas genéricas
T = TypeVar('T')


class ErrorResponse(BaseModel):
    """
    Modelo padrão para respostas de erro.
    """
    
    error: bool = Field(
        default=True,
        description="Indica que é uma resposta de erro"
    )
    message: str = Field(
        ...,
        description="Mensagem de erro legível"
    )
    error_code: Optional[str] = Field(
        None,
        description="Código específico do erro"
    )
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Detalhes adicionais sobre o erro"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp do erro"
    )


class SuccessResponse(BaseModel):
    """
    Modelo padrão para respostas de sucesso.
    """
    
    success: bool = Field(
        default=True,
        description="Indica que a operação foi bem-sucedida"
    )
    message: str = Field(
        default="Operação realizada com sucesso",
        description="Mensagem de sucesso"
    )
    data: Optional[Dict[str, Any]] = Field(
        None,
        description="Dados retornados pela operação"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp da resposta"
    )


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Modelo genérico para respostas paginadas.
    """
    
    items: List[T] = Field(
        ...,
        description="Lista de itens da página atual"
    )
    total: int = Field(
        ...,
        ge=0,
        description="Total de itens disponíveis"
    )
    page: int = Field(
        ...,
        ge=1,
        description="Página atual"
    )
    page_size: int = Field(
        ...,
        ge=1,
        description="Tamanho da página"
    )
    total_pages: int = Field(
        ...,
        ge=1,
        description="Total de páginas"
    )
    has_next: bool = Field(
        ...,
        description="Indica se há próxima página"
    )
    has_previous: bool = Field(
        ...,
        description="Indica se há página anterior"
    )


class HealthResponse(BaseModel):
    """
    Modelo para resposta de health check.
    """
    
    status: str = Field(
        default="healthy",
        description="Status da aplicação"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp do health check"
    )
    version: str = Field(
        ...,
        description="Versão da aplicação"
    )
    services: Dict[str, str] = Field(
        ...,
        description="Status dos serviços dependentes"
    )
    uptime: float = Field(
        ...,
        description="Tempo de atividade em segundos"
    )


class UsuarioResponse(TimestampedModel):
    """
    Modelo de resposta para dados de usuário.
    """
    
    id: str = Field(
        ...,
        description="ID único do usuário"
    )
    nome: str = Field(
        ...,
        description="Nome completo do usuário"
    )
    email: str = Field(
        ...,
        description="Email do usuário"
    )
    tipo_usuario: str = Field(
        ...,
        description="Tipo de usuário"
    )
    instituicao: Optional[str] = Field(
        None,
        description="Instituição de ensino"
    )
    status: StatusEnum = Field(
        default=StatusEnum.ACTIVE,
        description="Status do usuário"
    )
    configuracoes: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Configurações personalizadas"
    )
    estatisticas: Optional[Dict[str, Any]] = Field(
        None,
        description="Estatísticas do usuário"
    )


class LoginResponse(BaseModel):
    """
    Modelo de resposta para autenticação.
    """
    
    access_token: str = Field(
        ...,
        description="Token de acesso JWT"
    )
    token_type: str = Field(
        default="bearer",
        description="Tipo do token"
    )
    expires_in: int = Field(
        ...,
        description="Tempo de expiração em segundos"
    )
    refresh_token: Optional[str] = Field(
        None,
        description="Token para renovação"
    )
    usuario: UsuarioResponse = Field(
        ...,
        description="Dados do usuário autenticado"
    )


class PerguntaResponse(TimestampedModel):
    """
    Modelo de resposta para perguntas.
    """
    
    id: str = Field(
        ...,
        description="ID único da pergunta"
    )
    usuario_id: str = Field(
        ...,
        description="ID do usuário que fez a pergunta"
    )
    conteudo: str = Field(
        ...,
        description="Conteúdo da pergunta"
    )
    tipo_entrada: TipoMultimodalEnum = Field(
        ...,
        description="Tipo de entrada multimodal"
    )
    arquivos_anexos: List[str] = Field(
        default_factory=list,
        description="Arquivos anexados"
    )
    contexto: Optional[str] = Field(
        None,
        description="Contexto da pergunta"
    )
    disciplina: Optional[str] = Field(
        None,
        description="Disciplina relacionada"
    )
    nivel_dificuldade: Optional[NivelDificuldadeEnum] = Field(
        None,
        description="Nível de dificuldade"
    )
    status: StatusEnum = Field(
        default=StatusEnum.ACTIVE,
        description="Status da pergunta"
    )
    respostas_count: int = Field(
        default=0,
        description="Número de respostas recebidas"
    )
    metadados: Optional[MetadadosBase] = Field(
        None,
        description="Metadados adicionais"
    )


class RespostaResponse(TimestampedModel):
    """
    Modelo de resposta para respostas de perguntas.
    """
    
    id: str = Field(
        ...,
        description="ID único da resposta"
    )
    pergunta_id: str = Field(
        ...,
        description="ID da pergunta respondida"
    )
    usuario_id: str = Field(
        ...,
        description="ID do usuário que respondeu"
    )
    conteudo: str = Field(
        ...,
        description="Conteúdo da resposta"
    )
    confianca: Optional[float] = Field(
        None,
        description="Nível de confiança"
    )
    tempo_resposta: Optional[int] = Field(
        None,
        description="Tempo gasto para responder"
    )
    referencias: List[str] = Field(
        default_factory=list,
        description="Referências utilizadas"
    )
    status: StatusEnum = Field(
        default=StatusEnum.ACTIVE,
        description="Status da resposta"
    )
    avaliacoes_count: int = Field(
        default=0,
        description="Número de avaliações recebidas"
    )
    nota_media: Optional[float] = Field(
        None,
        description="Nota média das avaliações"
    )
    metadados: Optional[MetadadosBase] = Field(
        None,
        description="Metadados adicionais"
    )


class AvaliacaoResponse(TimestampedModel):
    """
    Modelo de resposta para avaliações.
    """
    
    id: str = Field(
        ...,
        description="ID único da avaliação"
    )
    resposta_id: str = Field(
        ...,
        description="ID da resposta avaliada"
    )
    avaliador_id: str = Field(
        ...,
        description="ID do avaliador"
    )
    nota: float = Field(
        ...,
        description="Nota atribuída"
    )
    tipo_avaliacao: TipoAvaliacaoEnum = Field(
        ...,
        description="Tipo de avaliação"
    )
    feedback: Optional[str] = Field(
        None,
        description="Feedback textual"
    )
    criterios: Dict[str, float] = Field(
        default_factory=dict,
        description="Critérios de avaliação"
    )
    sugestoes_melhoria: List[str] = Field(
        default_factory=list,
        description="Sugestões para melhoria"
    )
    status: StatusEnum = Field(
        default=StatusEnum.ACTIVE,
        description="Status da avaliação"
    )
    metadados: Optional[MetadadosBase] = Field(
        None,
        description="Metadados adicionais"
    )


class EmbeddingResponse(BaseModel):
    """
    Modelo de resposta para embeddings.
    """
    
    embedding: List[float] = Field(
        ...,
        description="Vetor de embedding gerado"
    )
    dimensoes: int = Field(
        ...,
        description="Número de dimensões do embedding"
    )
    modelo: str = Field(
        ...,
        description="Modelo utilizado para gerar o embedding"
    )
    tokens_utilizados: Optional[int] = Field(
        None,
        description="Número de tokens processados"
    )
    tempo_processamento: Optional[float] = Field(
        None,
        description="Tempo de processamento em segundos"
    )
    metadados: Optional[Dict[str, Any]] = Field(
        None,
        description="Metadados adicionais"
    )


class BuscaSemanticaResponse(BaseModel):
    """
    Modelo de resposta para busca semântica.
    """
    
    resultados: List[Dict[str, Any]] = Field(
        ...,
        description="Lista de resultados encontrados"
    )
    total_encontrados: int = Field(
        ...,
        description="Total de resultados encontrados"
    )
    tempo_busca: float = Field(
        ...,
        description="Tempo da busca em segundos"
    )
    query_original: str = Field(
        ...,
        description="Query original da busca"
    )
    score_threshold: float = Field(
        ...,
        description="Score mínimo utilizado"
    )
    metadados_busca: Optional[Dict[str, Any]] = Field(
        None,
        description="Metadados da busca realizada"
    )