"""
Modelos base para o sistema V-LABS.

Define classes base reutilizáveis e enums comuns para toda a aplicação.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Any, Dict, List
from pydantic import BaseModel as PydanticBaseModel, Field, ConfigDict


class BaseModel(PydanticBaseModel):
    """
    Modelo base para todos os modelos Pydantic do sistema.
    
    Configurações padrão para serialização, validação e documentação.
    """
    
    model_config = ConfigDict(
        # Permite campos extras em desenvolvimento, útil para extensibilidade
        extra="forbid",
        # Valida valores padrão
        validate_default=True,
        # Usa enum values ao invés de nomes
        use_enum_values=True,
        # Permite validação de tipos
        arbitrary_types_allowed=True,
        # Configuração de serialização
        str_strip_whitespace=True,
    )


class TimestampedModel(BaseModel):
    """
    Modelo base com campos de timestamp automáticos.
    
    Usado para entidades que precisam rastrear criação e modificação.
    """
    
    created_at: Optional[datetime] = Field(
        default=None,
        description="Data e hora de criação do registro"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Data e hora da última atualização"
    )


class PaginationParams(BaseModel):
    """
    Parâmetros padrão para paginação de listas.
    """
    
    page: int = Field(
        default=1,
        ge=1,
        description="Número da página (baseado em 1)"
    )
    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Quantidade de itens por página"
    )
    
    @property
    def skip(self) -> int:
        """Calcula quantos registros pular baseado na página atual."""
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """Retorna o limite de registros por página."""
        return self.page_size


class StatusEnum(str, Enum):
    """
    Status padrão para entidades do sistema.
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"
    DRAFT = "draft"


class TipoMultimodalEnum(str, Enum):
    """
    Tipos de entrada multimodal suportados pelo sistema.
    """
    TEXT = "text"
    IMAGE = "image"
    VOICE = "voice"
    EQUATION = "equation"
    MIXED = "mixed"


class NivelDificuldadeEnum(str, Enum):
    """
    Níveis de dificuldade para questões educacionais.
    """
    BASICO = "basico"
    INTERMEDIARIO = "intermediario"
    AVANCADO = "avancado"
    EXPERT = "expert"


class TipoAvaliacaoEnum(str, Enum):
    """
    Tipos de avaliação disponíveis no sistema.
    """
    FORMATIVA = "formativa"
    SOMATIVA = "somativa"
    DIAGNOSTICA = "diagnostica"
    AUTOAVALIACAO = "autoavaliacao"


class MetadadosBase(BaseModel):
    """
    Estrutura base para metadados flexíveis.
    """
    
    tags: Optional[List[str]] = Field(
        default_factory=list,
        description="Tags associadas ao recurso"
    )
    propriedades: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Propriedades customizadas"
    )
    versao: Optional[str] = Field(
        default="1.0",
        description="Versão do recurso"
    )


class ConfiguracaoIA(BaseModel):
    """
    Configurações para processamento de IA.
    """
    
    modelo: Optional[str] = Field(
        default="gpt-3.5-turbo",
        description="Modelo de IA a ser utilizado"
    )
    temperatura: Optional[float] = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Temperatura para geração de respostas"
    )
    max_tokens: Optional[int] = Field(
        default=1000,
        ge=1,
        le=4000,
        description="Máximo de tokens na resposta"
    )
    usar_contexto: bool = Field(
        default=True,
        description="Se deve usar contexto histórico"
    )