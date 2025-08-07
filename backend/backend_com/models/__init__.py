"""
Módulo de modelos Pydantic para o backend_com.

Exporta todos os modelos de request, response e base para uso
em toda a aplicação.
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
    ConfiguracaoIA
)

from .requests import (
    UsuarioRequest,
    LoginRequest,
    PerguntaRequest,
    RespostaRequest,
    AvaliacaoRequest,
    BuscaSemanticaRequest
)

from .responses import (
    UsuarioResponse,
    LoginResponse,
    PerguntaResponse,
    RespostaResponse,
    AvaliacaoResponse,
    BuscaSemanticaResponse,
    PaginatedResponse,
    SuccessResponse,
    ErrorResponse,
    HealthResponse
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
    "BuscaSemanticaRequest",
    
    "UsuarioResponse",
    "LoginResponse",
    "PerguntaResponse",
    "RespostaResponse",
    "AvaliacaoResponse",
    "BuscaSemanticaResponse",
    "PaginatedResponse",
    "SuccessResponse",
    "ErrorResponse",
    "HealthResponse"
]
