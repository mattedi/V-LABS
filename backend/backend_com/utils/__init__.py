"""
Utilitários e funções auxiliares para o backend_com.

Este módulo centraliza todas as funções utilitárias reutilizáveis
do sistema V-LABS.
"""

from .helpers import (
    # Funções gerais
    generate_uuid,
    format_timestamp,
    sanitize_string,
    validate_email_format,
    hash_password,
    verify_password,
    
    # Funções de validação
    validate_file_extension,
    validate_file_size,
    validate_json_structure,
    
    # Funções de formatação
    format_error_response,
    format_success_response,
    format_paginated_response,
    
    # Funções de conversão
    dict_to_object,
    object_to_dict,
    flatten_dict,
    unflatten_dict,
)

from .validators import (
    # Validadores Pydantic customizados
    validate_senha_forte,
    validate_cpf,
    validate_telefone_brasileiro,
    validate_url_completa,
    validate_json_field,
    validate_lista_nao_vazia,
)

from .formatters import (
    # Formatadores específicos
    format_cpf,
    format_telefone,
    format_cep,
    format_moeda_brasileira,
    format_tempo_decorrido,
    
    # Formatadores de dados educacionais
    format_nota,
    format_percentual,
    format_duracao_estudo,
)

from .security import (
    # Utilitários de segurança
    generate_secure_token,
    validate_token_format,
    sanitize_html_input,
    validate_file_security,
    check_rate_limit,
)

# Importa funções de logging diretamente
from .logging import (
    # Utilitários de logging
    setup_logger,
    configure_structured_logging,
    log_request,
    log_response,
    log_error,
    log_performance,
)

__all__ = [
    # Helpers gerais
    "generate_uuid",
    "format_timestamp", 
    "sanitize_string",
    "validate_email_format",
    "hash_password",
    "verify_password",
    "validate_file_extension",
    "validate_file_size",
    "validate_json_structure",
    "format_error_response",
    "format_success_response", 
    "format_paginated_response",
    "dict_to_object",
    "object_to_dict",
    "flatten_dict",
    "unflatten_dict",
    
    # Validadores
    "validate_senha_forte",
    "validate_cpf",
    "validate_telefone_brasileiro", 
    "validate_url_completa",
    "validate_json_field",
    "validate_lista_nao_vazia",
    
    # Formatadores
    "format_cpf",
    "format_telefone",
    "format_cep", 
    "format_moeda_brasileira",
    "format_tempo_decorrido",
    "format_nota",
    "format_percentual",
    "format_duracao_estudo",
    
    # Segurança
    "generate_secure_token",
    "validate_token_format",
    "sanitize_html_input",
    "validate_file_security",
    "check_rate_limit",
    
    # Logging
    "setup_logger",
    "configure_structured_logging",
    "log_request",
    "log_response", 
    "log_error",
    "log_performance",
]