"""
Utilitários de segurança para o backend_com.

Implementa funções para validação de tokens, sanitização
e verificações de segurança básicas.
"""

import re
import secrets
import hashlib
import html
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta


def generate_secure_token(length: int = 32) -> str:
    """
    Gera token seguro usando secrets.
    
    Args:
        length: Comprimento do token em bytes
        
    Returns:
        str: Token hexadecimal seguro
    """
    return secrets.token_hex(length)


def validate_token_format(token: str, expected_length: int = 64) -> bool:
    """
    Valida formato de token hexadecimal.
    
    Args:
        token: Token para validar
        expected_length: Comprimento esperado
        
    Returns:
        bool: True se formato for válido
    """
    if not token or not isinstance(token, str):
        return False
    
    # Verifica se é hexadecimal válido
    if not re.match(r'^[a-fA-F0-9]+$', token):
        return False
    
    # Verifica comprimento
    return len(token) == expected_length


def sanitize_html_input(text: str) -> str:
    """
    Sanitiza entrada HTML removendo tags perigosas.
    
    Args:
        text: Texto para sanitizar
        
    Returns:
        str: Texto sanitizado
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Escape HTML básico
    sanitized = html.escape(text)
    
    # Remove scripts inline e outros padrões perigosos
    dangerous_patterns = [
        r'javascript:',
        r'vbscript:',
        r'onload=',
        r'onerror=',
        r'onclick=',
        r'onmouseover=',
        r'<script',
        r'</script>',
        r'<iframe',
        r'<object',
        r'<embed',
    ]
    
    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
    
    return sanitized.strip()


def validate_file_security(filename: str, content_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Valida segurança de arquivo upload.
    
    Args:
        filename: Nome do arquivo
        content_type: Tipo MIME do conteúdo
        
    Returns:
        dict: Resultado da validação com detalhes
    """
    result = {
        "is_safe": True,
        "warnings": [],
        "errors": []
    }
    
    if not filename:
        result["is_safe"] = False
        result["errors"].append("Nome do arquivo é obrigatório")
        return result
    
    # Extensões perigosas
    dangerous_extensions = [
        '.exe', '.bat', '.cmd', '.com', '.pif', '.scr', '.vbs', '.js',
        '.jar', '.asp', '.php', '.py', '.rb', '.sh', '.pl'
    ]
    
    # Verifica extensão
    file_ext = '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    
    if file_ext in dangerous_extensions:
        result["is_safe"] = False
        result["errors"].append(f"Extensão {file_ext} não é permitida")
    
    # Extensões permitidas para contexto educacional
    allowed_extensions = [
        '.pdf', '.doc', '.docx', '.txt', '.rtf',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp',
        '.mp3', '.wav', '.mp4', '.avi', '.mov',
        '.xls', '.xlsx', '.ppt', '.pptx',
        '.zip', '.rar'
    ]
    
    if file_ext not in allowed_extensions:
        result["warnings"].append(f"Extensão {file_ext} não está na lista de permitidas")
    
    # Valida nome do arquivo
    if re.search(r'[<>:"/\\|?*]', filename):
        result["is_safe"] = False
        result["errors"].append("Nome do arquivo contém caracteres inválidos")
    
    # Verifica caracteres de controle
    if any(ord(char) < 32 for char in filename):
        result["is_safe"] = False
        result["errors"].append("Nome do arquivo contém caracteres de controle")
    
    # Verifica content-type se fornecido
    if content_type:
        safe_content_types = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain',
            'image/jpeg',
            'image/png',
            'image/gif',
            'audio/mpeg',
            'video/mp4'
        ]
        
        if content_type not in safe_content_types:
            result["warnings"].append(f"Content-type {content_type} não verificado")
    
    return result


def check_rate_limit(identifier: str, max_requests: int = 100, 
                    window_minutes: int = 60, storage: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Verifica rate limiting básico usando armazenamento em memória.
    
    Args:
        identifier: Identificador único (IP, user_id, etc.)
        max_requests: Máximo de requisições no período
        window_minutes: Janela de tempo em minutos
        storage: Dicionário para armazenar contadores (opcional)
        
    Returns:
        dict: Resultado da verificação
    """
    if storage is None:
        # Armazenamento global simples (apenas para desenvolvimento)
        if not hasattr(check_rate_limit, '_storage'):
            check_rate_limit._storage = {}
        storage = check_rate_limit._storage
    
    now = datetime.now()
    window_start = now - timedelta(minutes=window_minutes)
    
    # Limpa registros antigos
    if identifier in storage:
        storage[identifier] = [
            timestamp for timestamp in storage[identifier]
            if timestamp > window_start
        ]
    else:
        storage[identifier] = []
    
    # Verifica limite
    current_requests = len(storage[identifier])
    
    result = {
        "allowed": current_requests < max_requests,
        "current_requests": current_requests,
        "max_requests": max_requests,
        "reset_time": window_start + timedelta(minutes=window_minutes),
        "remaining_requests": max(0, max_requests - current_requests)
    }
    
    # Adiciona requisição atual se permitida
    if result["allowed"]:
        storage[identifier].append(now)
    
    return result


def hash_sensitive_data(data: str, salt: Optional[str] = None) -> str:
    """
    Gera hash de dados sensíveis usando SHA-256.
    
    Args:
        data: Dados para hash
        salt: Salt personalizado (opcional)
        
    Returns:
        str: Hash hexadecimal
    """
    if salt is None:
        salt = secrets.token_hex(16)
    
    combined = f"{salt}{data}"
    hash_obj = hashlib.sha256(combined.encode('utf-8'))
    
    return f"{salt}:{hash_obj.hexdigest()}"


def verify_sensitive_data_hash(data: str, hash_with_salt: str) -> bool:
    """
    Verifica hash de dados sensíveis.
    
    Args:
        data: Dados originais
        hash_with_salt: Hash com salt no formato "salt:hash"
        
    Returns:
        bool: True se hash for válido
    """
    try:
        salt, stored_hash = hash_with_salt.split(':', 1)
        
        combined = f"{salt}{data}"
        calculated_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        
        return calculated_hash == stored_hash
        
    except ValueError:
        return False


def validate_ip_address(ip: str) -> bool:
    """
    Valida formato de endereço IP (IPv4 ou IPv6).
    
    Args:
        ip: Endereço IP para validar
        
    Returns:
        bool: True se IP for válido
    """
    import ipaddress
    
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_ip_in_whitelist(ip: str, whitelist: List[str]) -> bool:
    """
    Verifica se IP está na lista de permitidos.
    
    Args:
        ip: Endereço IP
        whitelist: Lista de IPs permitidos
        
    Returns:
        bool: True se IP estiver na whitelist
    """
    import ipaddress
    
    try:
        client_ip = ipaddress.ip_address(ip)
        
        for allowed_ip in whitelist:
            try:
                # Suporta CIDR e IPs individuais
                if '/' in allowed_ip:
                    network = ipaddress.ip_network(allowed_ip, strict=False)
                    if client_ip in network:
                        return True
                else:
                    allowed = ipaddress.ip_address(allowed_ip)
                    if client_ip == allowed:
                        return True
            except ValueError:
                continue
        
        return False
        
    except ValueError:
        return False


def generate_csrf_token() -> str:
    """
    Gera token CSRF seguro.
    
    Returns:
        str: Token CSRF
    """
    return secrets.token_urlsafe(32)


def validate_user_agent(user_agent: str) -> Dict[str, Any]:
    """
    Valida e analisa User-Agent para detectar bots suspeitos.
    
    Args:
        user_agent: String do User-Agent
        
    Returns:
        dict: Análise do User-Agent
    """
    result = {
        "is_valid": True,
        "is_bot": False,
        "is_suspicious": False,
        "warnings": []
    }
    
    if not user_agent or len(user_agent.strip()) == 0:
        result["is_valid"] = False
        result["warnings"].append("User-Agent vazio")
        return result
    
    # Padrões de bots conhecidos
    bot_patterns = [
        r'bot', r'crawler', r'spider', r'scraper',
        r'wget', r'curl', r'python', r'requests'
    ]
    
    ua_lower = user_agent.lower()
    
    for pattern in bot_patterns:
        if re.search(pattern, ua_lower):
            result["is_bot"] = True
            break
    
    # Verifica padrões suspeitos
    if len(user_agent) < 10:
        result["is_suspicious"] = True
        result["warnings"].append("User-Agent muito curto")
    
    if len(user_agent) > 500:
        result["is_suspicious"] = True
        result["warnings"].append("User-Agent muito longo")
    
    # Verifica caracteres estranhos
    if re.search(r'[<>{}\\]', user_agent):
        result["is_suspicious"] = True
        result["warnings"].append("User-Agent contém caracteres suspeitos")
    
    return result