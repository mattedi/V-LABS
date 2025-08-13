# backend/backend_com/config.py
from typing import List
from pydantic import Field

# Detecta Pydantic v2 (pydantic-settings) e faz fallback para v1
try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
    _V2 = True
except ImportError:  # fallback p/ Pydantic v1
    from pydantic import BaseSettings  # type: ignore
    SettingsConfigDict = None  # só para type hints
    _V2 = False


class Settings(BaseSettings):
    # ----- App -----
    app_name: str = Field(default="V-LABS Backend Communication")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=True)
    environment: str = Field(default="development")

    # ----- Server -----
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000)

    # ----- CORS -----
    cors_origins: List[str] = Field(default=["http://localhost:3000", "http://localhost:5173"])
    cors_methods: List[str] = Field(default=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    cors_headers: List[str] = Field(default=["*"])

    # ----- Integração Backend_BD -----
    backend_bd_url: str = Field(default="http://127.0.0.1:8001")
    backend_bd_timeout: int = Field(default=30)

    # ----- Logs -----
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Configuração de leitura de .env (v2) ou (v1)
    if _V2:
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            case_sensitive=False,
            extra="ignore",
        )
    else:  # Pydantic v1
        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
            case_sensitive = False


settings = Settings()


def get_settings() -> Settings:
    return settings


def get_cors_config() -> dict:
    """
    Converte as listas para o formato esperado pelo CORS middleware.
    (Se você quiser ler CORS de uma env CSV, basta fazer o split aqui.)
    """
    return {
        "allow_origins": settings.cors_origins,
        "allow_credentials": True,
        "allow_methods": settings.cors_methods,
        "allow_headers": settings.cors_headers,
    }
