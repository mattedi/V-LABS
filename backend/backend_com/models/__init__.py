"""
Modelos do backend_com.

Exporta todos os modelos para facilitar importação.
"""

from .base import (
    BaseModel,
    TimestampedModel,
    PaginationParams,
    StatusEnum,
    TipoMultimodalEnum,
    NivelDificuldadeEnum,
    TipoAvaliacaoEnum,
    MetadadosBase,
    ConfiguracaoIA,
)

from .requests import (
    UsuarioRequest,
    LoginRequest,
    PerguntaRequest,
    RespostaRequest,
    AvaliacaoRequest,
    EmbeddingRequest,
    BuscaSemanticaRequest,
)

from .responses import (
    ErrorResponse,
    SuccessResponse,
    PaginatedResponse,
    HealthResponse,
    UsuarioResponse,
    LoginResponse,
    PerguntaResponse,
    RespostaResponse,
    AvaliacaoResponse,
    EmbeddingResponse,
    BuscaSemanticaResponse,
)

__all__ = [
    "BaseModel",
    "TimestampedModel", 
    "PaginationParams",
    "StatusEnum",
    "TipoMultimodalEnum",
    "NivelDificuldadeEnum",
    "TipoAvaliacaoEnum",
    "MetadadosBase",
    "ConfiguracaoIA",
    "UsuarioRequest",
    "LoginRequest",
    "PerguntaRequest",
    "RespostaRequest",
    "AvaliacaoRequest",
    "EmbeddingRequest",
    "BuscaSemanticaRequest",
    "ErrorResponse",
    "SuccessResponse",
    "PaginatedResponse",
    "HealthResponse",
    "UsuarioResponse",
    "LoginResponse",
    "PerguntaResponse",
    "RespostaResponse",
    "AvaliacaoResponse",
    "EmbeddingResponse",
    "BuscaSemanticaResponse",
]
