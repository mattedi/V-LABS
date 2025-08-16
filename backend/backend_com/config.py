"""
Configuração central da camada Backend Communication.

✔️ Compatível com Pydantic v2 (+ pydantic-settings)  
✔️ Fallback transparente para Pydantic v1  
✔️ Sem imports duplicados nem advertências do runtime
"""

from __future__ import annotations
from typing import List, Optional

# ── Import condicional compatível Pydantic v1/v2 ─────────────────────────
try:  # Pydantic v2
    from pydantic_settings import BaseSettings, SettingsConfigDict
    _V2 = True
except ImportError:  # fallback para Pydantic v1
    from pydantic import BaseSettings  # type: ignore
    SettingsConfigDict = None
    _V2 = False

from pydantic import Field, MongoDsn, AnyHttpUrl


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ Modelo de settings                                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
class Settings(BaseSettings):
    # ── App ────────────────────────────────────────────────────────────────
    app_name: str = Field(default="V-LABS Backend Communication")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=True)
    environment: str = Field(default="development")

    # ── Servidor ───────────────────────────────────────────────────────────
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000)

    # ── CORS ───────────────────────────────────────────────────────────────
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"]
    )
    cors_methods: List[str] = Field(default=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    cors_headers: List[str] = Field(default=["*"])

    # ── Integração Backend_BD ───────────────────────────────────────────────
    backend_bd_url: AnyHttpUrl = Field(default="http://127.0.0.1:8001")
    backend_bd_timeout: int = Field(default=30)

    # ── Mongo / Qdrant (exemplo) ────────────────────────────────────────────
    mongodb_uri: MongoDsn = Field(default="mongodb://localhost:27017")
    mongodb_db: str = Field(default="vlabs")
    qdrant_url: AnyHttpUrl = Field(default="http://localhost:6333")
    qdrant_api_key: Optional[str] = Field(default=None)

    # ── Logs ───────────────────────────────────────────────────────────────
    log_level: str = Field(default="INFO")
    log_format: str = Field(
        default="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    # ── Config Pydantic ─────────────────────────────────────────────────────
    if _V2:  # Pydantic v2
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            case_sensitive=False,
            extra="ignore",
        )
    else:  # Pydantic v1
        class Config:  # noqa: D401
            env_file = ".env"
            env_file_encoding = "utf-8"
            case_sensitive = False


# Instância única carregada no import
settings = Settings()


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ Helpers públicos                                                          ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
def get_settings() -> Settings:
    """Retorna a instância singleton de configurações."""
    return settings


def get_cors_config() -> dict:
    """Retorna dicionário pronto para CORSMiddleware."""
    return {
        "allow_origins": settings.cors_origins,
        "allow_credentials": True,
        "allow_methods": settings.cors_methods,
        "allow_headers": settings.cors_headers,
    }
