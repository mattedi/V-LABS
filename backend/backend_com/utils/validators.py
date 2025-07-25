"""
Validadores customizados para campos Pydantic.

Implementa validadores específicos para dados brasileiros e regras
de negócio do sistema educacional V-LABS.
"""

import re
import json
from typing import Any, List
from urllib.parse import urlparse
from pydantic import validator


def validate_senha_forte(senha: str) -> str:
    """
    Valida se senha atende critérios de segurança.
    
    Critérios:
    - Mínimo 8 caracteres
    - Pelo menos 1 letra minúscula
    - Pelo menos 1 letra maiúscula  
    - Pelo menos 1 número
    - Pelo menos 1 caractere especial
    
    Args:
        senha: Senha para validar
        
    Returns:
        str: Senha validada
        
    Raises:
        ValueError: Se senha não atender critérios
    """
    if len(senha) < 8:
        raise ValueError("Senha deve ter pelo menos 8 caracteres")
    
    if not re.search(r'[a-z]', senha):
        raise ValueError("Senha deve conter pelo menos uma letra minúscula")
    
    if not re.search(r'[A-Z]', senha):
        raise ValueError("Senha deve conter pelo menos uma letra maiúscula")
    
    if not re.search(r'\d', senha):
        raise ValueError("Senha deve conter pelo menos um número")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        raise ValueError("Senha deve conter pelo menos um caractere especial")
    
    # Verifica padrões fracos comuns
    padroes_fracos = [
        r'123456',
        r'password',
        r'qwerty',
        r'abc123',
        r'admin',
        r'senha',
        r'123abc'
    ]
    
    senha_lower = senha.lower()
    for padrao in padroes_fracos:
        if padrao in senha_lower:
            raise ValueError(f"Senha não pode conter padrões comuns como '{padrao}'")
    
    return senha


def validate_cpf(cpf: str) -> str:
    """
    Valida CPF brasileiro usando algoritmo oficial.
    
    Args:
        cpf: String do CPF (com ou sem formatação)
        
    Returns:
        str: CPF limpo (apenas números)
        
    Raises:
        ValueError: Se CPF for inválido
    """
    # Remove formatação
    cpf_limpo = re.sub(r'[^\d]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf_limpo) != 11:
        raise ValueError("CPF deve ter 11 dígitos")
    
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if cpf_limpo == cpf_limpo[0] * 11:
        raise ValueError("CPF não pode ter todos os dígitos iguais")
    
    # Validação do primeiro dígito verificador
    soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf_limpo[9]) != digito1:
        raise ValueError("CPF inválido - primeiro dígito verificador")
    
    # Validação do segundo dígito verificador
    soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    if int(cpf_limpo[10]) != digito2:
        raise ValueError("CPF inválido - segundo dígito verificador")
    
    return cpf_limpo


def validate_telefone_brasileiro(telefone: str) -> str:
    """
    Valida número de telefone brasileiro.
    
    Aceita formatos:
    - (11) 99999-9999
    - 11999999999
    - +5511999999999
    
    Args:
        telefone: Número de telefone
        
    Returns:
        str: Telefone limpo
        
    Raises:
        ValueError: Se telefone for inválido
    """
    # Remove formatação
    telefone_limpo = re.sub(r'[^\d]', '', telefone)
    
    # Remove código do país se presente
    if telefone_limpo.startswith('55') and len(telefone_limpo) == 13:
        telefone_limpo = telefone_limpo[2:]
    
    # Verifica se tem 10 ou 11 dígitos (com ou sem 9º dígito)
    if len(telefone_limpo) not in [10, 11]:
        raise ValueError("Telefone deve ter 10 ou 11 dígitos")
    
    # Verifica código de área válido (11-99)
    codigo_area = int(telefone_limpo[:2])
    if codigo_area < 11 or codigo_area > 99:
        raise ValueError("Código de área inválido")
    
    # Se tem 11 dígitos, verifica se o 9º dígito é 9
    if len(telefone_limpo) == 11 and telefone_limpo[2] != '9':
        raise ValueError("Para celulares, o terceiro dígito deve ser 9")
    
    return telefone_limpo


def validate_url_completa(url: str) -> str:
    """
    Valida URL completa com esquema e domínio.
    
    Args:
        url: URL para validar
        
    Returns:
        str: URL validada
        
    Raises:
        ValueError: Se URL for inválida
    """
    try:
        parsed = urlparse(url)
        
        if not parsed.scheme:
            raise ValueError("URL deve incluir esquema (http/https)")
        
        if parsed.scheme not in ['http', 'https']:
            raise ValueError("Esquema deve ser http ou https")
        
        if not parsed.netloc:
            raise ValueError("URL deve incluir domínio válido")
        
        # Verifica se domínio tem pelo menos um ponto
        if '.' not in parsed.netloc:
            raise ValueError("Domínio deve ser válido")
        
        return url
        
    except Exception as e:
        raise ValueError(f"URL inválida: {str(e)}")


def validate_json_field(valor: str) -> dict:
    """
    Valida e converte string JSON em dicionário.
    
    Args:
        valor: String JSON
        
    Returns:
        dict: Dicionário parseado
        
    Raises:
        ValueError: Se JSON for inválido
    """
    if not valor or not isinstance(valor, str):
        return {}
    
    try:
        parsed = json.loads(valor)
        if not isinstance(parsed, dict):
            raise ValueError("JSON deve ser um objeto")
        return parsed
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON inválido: {str(e)}")


def validate_lista_nao_vazia(lista: List[Any]) -> List[Any]:
    """
    Valida se lista não está vazia.
    
    Args:
        lista: Lista para validar
        
    Returns:
        List[Any]: Lista validada
        
    Raises:
        ValueError: Se lista estiver vazia
    """
    if not lista or len(lista) == 0:
        raise ValueError("Lista não pode estar vazia")
    
    return lista


def validate_nota_educacional(nota: float) -> float:
    """
    Valida nota educacional no sistema brasileiro (0-10).
    
    Args:
        nota: Nota para validar
        
    Returns:
        float: Nota validada
        
    Raises:
        ValueError: Se nota for inválida
    """
    if not isinstance(nota, (int, float)):
        raise ValueError("Nota deve ser um número")
    
    if nota < 0 or nota > 10:
        raise ValueError("Nota deve estar entre 0 e 10")
    
    # Limita a 2 casas decimais
    return round(float(nota), 2)


def validate_email_educacional(email: str) -> str:
    """
    Valida email educacional com domínios específicos.
    
    Args:
        email: Email para validar
        
    Returns:
        str: Email validado
        
    Raises:
        ValueError: Se email não for educacional
    """
    from .helpers import validate_email_format
    
    if not validate_email_format(email):
        raise ValueError("Formato de email inválido")
    
    # Lista de domínios educacionais aceitos
    dominios_educacionais = [
        '.edu.br',
        '.edu',
        '.ac.br',
        'unifesp.br',
        'usp.br',
        'unicamp.br',
        'ufrj.br',
        'ufsc.br',
        'puc-rio.br',
        'fgv.br'
    ]
    
    email_lower = email.lower()
    
    # Verifica se termina com domínio educacional
    if not any(email_lower.endswith(dom) for dom in dominios_educacionais):
        # Para desenvolvimento, permite emails comuns
        if not any(email_lower.endswith(dom) for dom in [
            'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com'
        ]):
            raise ValueError("Email deve ser de instituição educacional")
    
    return email


def validate_duracao_em_minutos(duracao: int) -> int:
    """
    Valida duração em minutos para atividades educacionais.
    
    Args:
        duracao: Duração em minutos
        
    Returns:
        int: Duração validada
        
    Raises:
        ValueError: Se duração for inválida
    """
    if not isinstance(duracao, int):
        raise ValueError("Duração deve ser um número inteiro")
    
    if duracao < 1:
        raise ValueError("Duração deve ser pelo menos 1 minuto")
    
    if duracao > 600:  # 10 horas
        raise ValueError("Duração não pode exceder 10 horas (600 minutos)")
    
    return duracao


def validate_nivel_escolar(nivel: str) -> str:
    """
    Valida nível escolar brasileiro.
    
    Args:
        nivel: Nível escolar
        
    Returns:
        str: Nível validado
        
    Raises:
        ValueError: Se nível for inválido
    """
    niveis_validos = [
        'educacao_infantil',
        'ensino_fundamental_1',
        'ensino_fundamental_2', 
        'ensino_medio',
        'ensino_superior',
        'pos_graduacao',
        'mestrado',
        'doutorado'
    ]
    
    if nivel not in niveis_validos:
        raise ValueError(f"Nível escolar deve ser um dos: {', '.join(niveis_validos)}")
    
    return nivel