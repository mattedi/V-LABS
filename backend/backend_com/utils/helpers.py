"""
Funções auxiliares gerais para o backend_com.

Implementa utilitários comuns para manipulação de dados, validação
e formatação utilizados em todo o sistema.
"""

import uuid
import json
import re
import hashlib
import secrets
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from email_validator import validate_email, EmailNotValidError
import bcrypt


def generate_uuid() -> str:
    """
    Gera um UUID4 único como string.
    
    Returns:
        str: UUID único no formato string
    """
    return str(uuid.uuid4())


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """
    Formata um datetime para string ISO 8601 com timezone UTC.
    
    Args:
        dt: Datetime para formatar. Se None, usa datetime atual.
        
    Returns:
        str: String formatada em ISO 8601
    """
    if dt is None:
        dt = datetime.now(timezone.utc)
    
    return dt.isoformat()


def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitiza uma string removendo caracteres perigosos e limitando tamanho.
    
    Args:
        text: String para sanitizar
        max_length: Tamanho máximo (opcional)
        
    Returns:
        str: String sanitizada
    """
    if not isinstance(text, str):
        return ""
    
    # Remove caracteres de controle e espaços extras
    sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    sanitized = ' '.join(sanitized.split())
    
    # Limita tamanho se especificado
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length].strip()
    
    return sanitized


def validate_email_format(email: str) -> bool:
    """
    Valida formato de email usando biblioteca robusta.
    
    Args:
        email: Email para validar
        
    Returns:
        bool: True se email for válido
    """
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def hash_password(password: str) -> str:
    """
    Gera hash seguro da senha usando bcrypt.
    
    Args:
        password: Senha em texto plano
        
    Returns:
        str: Hash da senha
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """
    Verifica se a senha corresponde ao hash.
    
    Args:
        password: Senha em texto plano
        hashed: Hash armazenado
        
    Returns:
        bool: True se senha for válida
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False


def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Valida se extensão do arquivo é permitida.
    
    Args:
        filename: Nome do arquivo
        allowed_extensions: Lista de extensões permitidas (ex: ['.jpg', '.png'])
        
    Returns:
        bool: True se extensão for permitida
    """
    if not filename or '.' not in filename:
        return False
    
    extension = '.' + filename.rsplit('.', 1)[1].lower()
    return extension in [ext.lower() for ext in allowed_extensions]


def validate_file_size(file_size: int, max_size_mb: int) -> bool:
    """
    Valida se tamanho do arquivo está dentro do limite.
    
    Args:
        file_size: Tamanho do arquivo em bytes
        max_size_mb: Tamanho máximo em MB
        
    Returns:
        bool: True se tamanho for válido
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_size <= max_size_bytes


def validate_json_structure(data: str, expected_keys: List[str]) -> bool:
    """
    Valida se JSON possui estrutura esperada.
    
    Args:
        data: String JSON para validar
        expected_keys: Chaves obrigatórias
        
    Returns:
        bool: True se estrutura for válida
    """
    try:
        parsed = json.loads(data)
        if not isinstance(parsed, dict):
            return False
        
        return all(key in parsed for key in expected_keys)
    except (json.JSONDecodeError, TypeError):
        return False


def format_error_response(message: str, error_code: Optional[str] = None, 
                         details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Formata resposta de erro padronizada.
    
    Args:
        message: Mensagem de erro
        error_code: Código específico do erro
        details: Detalhes adicionais
        
    Returns:
        dict: Resposta de erro formatada
    """
    return {
        "error": True,
        "message": sanitize_string(message, 500),
        "error_code": error_code,
        "details": details or {},
        "timestamp": format_timestamp()
    }


def format_success_response(message: str = "Operação realizada com sucesso",
                          data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Formata resposta de sucesso padronizada.
    
    Args:
        message: Mensagem de sucesso
        data: Dados da resposta
        
    Returns:
        dict: Resposta de sucesso formatada
    """
    return {
        "success": True,
        "message": sanitize_string(message, 500),
        "data": data or {},
        "timestamp": format_timestamp()
    }


def format_paginated_response(items: List[Any], total: int, page: int, 
                            page_size: int) -> Dict[str, Any]:
    """
    Formata resposta paginada padronizada.
    
    Args:
        items: Lista de itens da página
        total: Total de itens
        page: Página atual
        page_size: Tamanho da página
        
    Returns:
        dict: Resposta paginada formatada
    """
    total_pages = max(1, (total + page_size - 1) // page_size)
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1
    }


def dict_to_object(data: Dict[str, Any]) -> Any:
    """
    Converte dicionário para objeto com notação de ponto.
    
    Args:
        data: Dicionário para converter
        
    Returns:
        Any: Objeto com atributos
    """
    class DictObject:
        def __init__(self, dictionary):
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    value = dict_to_object(value)
                elif isinstance(value, list):
                    value = [dict_to_object(item) if isinstance(item, dict) else item 
                            for item in value]
                setattr(self, key, value)
    
    return DictObject(data)


def object_to_dict(obj: Any, exclude_private: bool = True) -> Dict[str, Any]:
    """
    Converte objeto para dicionário.
    
    Args:
        obj: Objeto para converter
        exclude_private: Se deve excluir atributos privados
        
    Returns:
        dict: Dicionário com atributos do objeto
    """
    if hasattr(obj, '__dict__'):
        result = {}
        for key, value in obj.__dict__.items():
            if exclude_private and key.startswith('_'):
                continue
            
            if hasattr(value, '__dict__'):
                result[key] = object_to_dict(value, exclude_private)
            elif isinstance(value, list):
                result[key] = [
                    object_to_dict(item, exclude_private) if hasattr(item, '__dict__') 
                    else item for item in value
                ]
            else:
                result[key] = value
        return result
    
    return obj


def flatten_dict(data: Dict[str, Any], parent_key: str = '', 
                separator: str = '.') -> Dict[str, Any]:
    """
    Achata dicionário aninhado em estrutura plana.
    
    Args:
        data: Dicionário para achatar
        parent_key: Chave pai (usado na recursão)
        separator: Separador para chaves aninhadas
        
    Returns:
        dict: Dicionário achatado
    """
    items = []
    
    for key, value in data.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, separator).items())
        else:
            items.append((new_key, value))
    
    return dict(items)


def unflatten_dict(data: Dict[str, Any], separator: str = '.') -> Dict[str, Any]:
    """
    Reconstrói dicionário aninhado a partir de estrutura plana.
    
    Args:
        data: Dicionário achatado
        separator: Separador usado nas chaves
        
    Returns:
        dict: Dicionário com estrutura aninhada
    """
    result = {}
    
    for key, value in data.items():
        keys = key.split(separator)
        current = result
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
    
    return result


def calculate_pagination_info(total_items: int, page: int, page_size: int) -> Dict[str, Any]:
    """
    Calcula informações de paginação.
    
    Args:
        total_items: Total de itens
        page: Página atual
        page_size: Itens por página
        
    Returns:
        dict: Informações de paginação
    """
    total_pages = max(1, (total_items + page_size - 1) // page_size)
    skip = (page - 1) * page_size
    
    return {
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "page_size": page_size,
        "skip": skip,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "next_page": page + 1 if page < total_pages else None,
        "previous_page": page - 1 if page > 1 else None
    }