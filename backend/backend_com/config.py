"""
Configurações centralizadas do backend_com - VERSÃO CORRIGIDA

Este módulo gerencia todas as configurações do sistema através de variáveis
de ambiente, fornecendo valores padrão seguros para desenvolvimento.
"""

import os
from typing import Optional
from pydantic import Field

# CORREÇÃO: Import correto para Pydantic v2
try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback para versões mais antigas
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação usando Pydantic BaseSettings."""
    
    # === CONFIGURAÇÕES BÁSICAS ===
    app_name: str = Field(default="V-LABS Backend Communication", description="Nome da aplicação")
    app_version: str = Field(default="1.0.0", description="Versão da aplicação")
    debug: bool = Field(default=False, description="Modo debug")
    environment: str = Field(default="development", description="Ambiente de execução")
    
    # === SERVIDOR ===
    host: str = Field(default="0.0.0.0", description="Host do servidor")
    port: int = Field(default=8000, description="Porta do servidor")
    
    # === CORS ===
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Origens permitidas para CORS"
    )
    cors_methods: list[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="Métodos HTTP permitidos"
    )
    cors_headers: list[str] = Field(
        default=["*"],
        description="Headers permitidos"
    )
    
    # === BACKEND_BD (PERSISTÊNCIA) ===
    backend_bd_url: str = Field(
        default="http://localhost:8001",
        description="URL do backend de persistência"
    )
    backend_bd_timeout: int = Field(
        default=30,
        description="Timeout para requisições ao backend_bd em segundos"
    )
    
    # === LOGS ===
    log_level: str = Field(default="INFO", description="Nível de log")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Formato do log"
    )
    
    # === RATE LIMITING (FUTURO) ===
    rate_limit_requests: int = Field(default=100, description="Limite de requisições por minuto")
    rate_limit_window: int = Field(default=60, description="Janela de tempo em segundos")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Instância global das configurações
settings = Settings()


def get_settings() -> Settings:
    """
    Factory function para obter instância das configurações.
    
    Útil para injeção de dependência no FastAPI e testes.
    
    Returns:
        Settings: Instância das configurações
    """
    return settings


def is_development() -> bool:
    """
    Verifica se está em ambiente de desenvolvimento.
    
    Returns:
        bool: True se estiver em desenvolvimento
    """
    return settings.environment.lower() in ["development", "dev", "local"]


def is_production() -> bool:
    """
    Verifica se está em ambiente de produção.
    
    Returns:
        bool: True se estiver em produção
    """
    return settings.environment.lower() in ["production", "prod"]


def get_cors_config() -> dict:
    """
    Retorna configuração de CORS formatada para FastAPI.
    
    Returns:
        dict: Configuração de CORS
    """
    return {
        "allow_origins": settings.cors_origins,
        "allow_credentials": True,
        "allow_methods": settings.cors_methods,
        "allow_headers": settings.cors_headers,
    }