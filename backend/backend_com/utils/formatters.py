"""
Formatadores de dados específicos para o sistema V-LABS.

Implementa funções de formatação para dados brasileiros e
contexto educacional.
"""

import re
from datetime import datetime, timedelta
from typing import Optional, Union
from decimal import Decimal, ROUND_HALF_UP


def format_cpf(cpf: str) -> str:
    """
    Formata CPF no padrão brasileiro (000.000.000-00).
    
    Args:
        cpf: CPF limpo (apenas números)
        
    Returns:
        str: CPF formatado
    """
    # Remove caracteres não numéricos
    cpf_limpo = re.sub(r'[^\d]', '', cpf)
    
    if len(cpf_limpo) != 11:
        return cpf  # Retorna original se inválido
    
    return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"


def format_telefone(telefone: str) -> str:
    """
    Formata telefone brasileiro no padrão (00) 00000-0000.
    
    Args:
        telefone: Telefone limpo (apenas números)
        
    Returns:
        str: Telefone formatado
    """
    # Remove caracteres não numéricos
    telefone_limpo = re.sub(r'[^\d]', '', telefone)
    
    if len(telefone_limpo) == 10:
        # Telefone fixo: (00) 0000-0000
        return f"({telefone_limpo[:2]}) {telefone_limpo[2:6]}-{telefone_limpo[6:]}"
    elif len(telefone_limpo) == 11:
        # Celular: (00) 00000-0000
        return f"({telefone_limpo[:2]}) {telefone_limpo[2:7]}-{telefone_limpo[7:]}"
    
    return telefone  # Retorna original se inválido


def format_cep(cep: str) -> str:
    """
    Formata CEP brasileiro no padrão 00000-000.
    
    Args:
        cep: CEP limpo (apenas números)
        
    Returns:
        str: CEP formatado
    """
    # Remove caracteres não numéricos
    cep_limpo = re.sub(r'[^\d]', '', cep)
    
    if len(cep_limpo) != 8:
        return cep  # Retorna original se inválido
    
    return f"{cep_limpo[:5]}-{cep_limpo[5:]}"


def format_moeda_brasileira(valor: Union[float, int, Decimal], 
                          incluir_simbolo: bool = True) -> str:
    """
    Formata valor monetário no padrão brasileiro.
    
    Args:
        valor: Valor para formatar
        incluir_simbolo: Se deve incluir símbolo R$
        
    Returns:
        str: Valor formatado (ex: R$ 1.234,56)
    """
    try:
        # Converte para Decimal para precisão
        if isinstance(valor, Decimal):
            decimal_valor = valor
        else:
            decimal_valor = Decimal(str(valor))
        
        # Arredonda para 2 casas decimais
        decimal_valor = decimal_valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Converte para string e separa parte inteira e decimal
        valor_str = str(decimal_valor)
        if '.' in valor_str:
            parte_inteira, parte_decimal = valor_str.split('.')
        else:
            parte_inteira, parte_decimal = valor_str, '00'
        
        # Garante 2 dígitos decimais
        parte_decimal = parte_decimal.ljust(2, '0')[:2]
        
        # Formata parte inteira com separadores de milhares
        parte_inteira_formatada = ""
        for i, digito in enumerate(reversed(parte_inteira)):
            if i > 0 and i % 3 == 0:
                parte_inteira_formatada = "." + parte_inteira_formatada
            parte_inteira_formatada = digito + parte_inteira_formatada
        
        # Monta valor final
        valor_formatado = f"{parte_inteira_formatada},{parte_decimal}"
        
        if incluir_simbolo:
            return f"R$ {valor_formatado}"
        
        return valor_formatado
        
    except (ValueError, TypeError):
        return str(valor)


def format_tempo_decorrido(inicio: datetime, fim: Optional[datetime] = None) -> str:
    """
    Formata tempo decorrido em formato legível.
    
    Args:
        inicio: Datetime de início
        fim: Datetime de fim (padrão: agora)
        
    Returns:
        str: Tempo formatado (ex: "2h 30min", "45 segundos")
    """
    if fim is None:
        fim = datetime.now(inicio.tzinfo or None)
    
    delta = fim - inicio
    total_segundos = int(delta.total_seconds())
    
    if total_segundos < 0:
        return "0 segundos"
    
    # Calcula componentes de tempo
    dias = total_segundos // 86400
    horas = (total_segundos % 86400) // 3600
    minutos = (total_segundos % 3600) // 60
    segundos = total_segundos % 60
    
    # Formata baseado na duração
    if dias > 0:
        if horas > 0:
            return f"{dias}d {horas}h"
        return f"{dias} dia{'s' if dias > 1 else ''}"
    
    if horas > 0:
        if minutos > 0:
            return f"{horas}h {minutos}min"
        return f"{horas} hora{'s' if horas > 1 else ''}"
    
    if minutos > 0:
        if segundos > 0 and minutos < 5:  # Mostra segundos apenas para durações curtas
            return f"{minutos}min {segundos}s"
        return f"{minutos} minuto{'s' if minutos > 1 else ''}"
    
    return f"{segundos} segundo{'s' if segundos != 1 else ''}"


def format_nota(nota: Union[float, int], escala_maxima: float = 10.0) -> str:
    """
    Formata nota educacional com precisão adequada.
    
    Args:
        nota: Nota para formatar
        escala_maxima: Valor máximo da escala
        
    Returns:
        str: Nota formatada (ex: "8,5", "10,0")
    """
    try:
        nota_decimal = Decimal(str(nota))
        nota_decimal = nota_decimal.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        
        # Formata com vírgula decimal brasileira
        nota_str = str(nota_decimal).replace('.', ',')
        
        # Garante pelo menos uma casa decimal
        if ',' not in nota_str:
            nota_str += ",0"
        
        return nota_str
        
    except (ValueError, TypeError):
        return str(nota)


def format_percentual(valor: Union[float, int], casas_decimais: int = 1) -> str:
    """
    Formata valor como percentual brasileiro.
    
    Args:
        valor: Valor para formatar (0-1 ou 0-100)
        casas_decimais: Número de casas decimais
        
    Returns:
        str: Percentual formatado (ex: "85,5%")
    """
    try:
        # Se valor está entre 0-1, converte para 0-100
        if 0 <= valor <= 1:
            valor_percentual = valor * 100
        else:
            valor_percentual = valor
        
        # Arredonda conforme casas decimais especificadas
        formato = f"0.{'0' * casas_decimais}f"
        valor_formatado = format(valor_percentual, formato)
        
        # Substitui ponto por vírgula
        valor_formatado = valor_formatado.replace('.', ',')
        
        return f"{valor_formatado}%"
        
    except (ValueError, TypeError):
        return str(valor)


def format_duracao_estudo(minutos: int) -> str:
    """
    Formata duração de estudo em formato educacional legível.
    
    Args:
        minutos: Duração em minutos
        
    Returns:
        str: Duração formatada (ex: "1h 30min", "45min")
    """
    if minutos < 0:
        return "0min"
    
    horas = minutos // 60
    mins_restantes = minutos % 60
    
    if horas > 0:
        if mins_restantes > 0:
            return f"{horas}h {mins_restantes}min"
        return f"{horas}h"
    
    return f"{minutos}min"


def format_nivel_dificuldade(nivel: str) -> str:
    """
    Formata nível de dificuldade para exibição.
    
    Args:
        nivel: Nível de dificuldade
        
    Returns:
        str: Nível formatado
    """
    mapeamento_niveis = {
        'basico': 'Básico',
        'intermediario': 'Intermediário',
        'avancado': 'Avançado',
        'expert': 'Expert'
    }
    
    return mapeamento_niveis.get(nivel.lower(), nivel.title())


def format_tipo_usuario(tipo: str) -> str:
    """
    Formata tipo de usuário para exibição.
    
    Args:
        tipo: Tipo de usuário
        
    Returns:
        str: Tipo formatado
    """
    mapeamento_tipos = {
        'student': 'Estudante',
        'teacher': 'Professor',
        'admin': 'Administrador',
        'tutor': 'Tutor',
        'coordinator': 'Coordenador'
    }
    
    return mapeamento_tipos.get(tipo.lower(), tipo.title())


def format_disciplina(disciplina: str) -> str:
    """
    Formata nome de disciplina para exibição consistente.
    
    Args:
        disciplina: Nome da disciplina
        
    Returns:
        str: Disciplina formatada
    """
    # Remove underscores e hífens, capitaliza palavras
    disciplina_limpa = disciplina.replace('_', ' ').replace('-', ' ')
    
    # Capitaliza cada palavra, mas preserva artigos/preposições minúsculas
    palavras_minusculas = {'de', 'da', 'do', 'das', 'dos', 'e', 'em', 'na', 'no', 'para'}
    
    palavras = disciplina_limpa.split()
    palavras_formatadas = []
    
    for i, palavra in enumerate(palavras):
        if i == 0 or palavra.lower() not in palavras_minusculas:
            palavras_formatadas.append(palavra.capitalize())
        else:
            palavras_formatadas.append(palavra.lower())
    
    return ' '.join(palavras_formatadas)


def format_data_brasileira(data: datetime, incluir_hora: bool = False) -> str:
    """
    Formata data no padrão brasileiro.
    
    Args:
        data: Data para formatar
        incluir_hora: Se deve incluir horário
        
    Returns:
        str: Data formatada (ex: "15/03/2024" ou "15/03/2024 14:30")
    """
    try:
        if incluir_hora:
            return data.strftime("%d/%m/%Y %H:%M")
        return data.strftime("%d/%m/%Y")
        
    except (ValueError, AttributeError):
        return str(data)


def format_tamanho_arquivo(bytes_size: int) -> str:
    """
    Formata tamanho de arquivo em unidades legíveis.
    
    Args:
        bytes_size: Tamanho em bytes
        
    Returns:
        str: Tamanho formatado (ex: "1,5 MB", "350 KB")
    """
    if bytes_size < 1024:
        return f"{bytes_size} B"
    
    elif bytes_size < 1024 * 1024:
        kb_size = bytes_size / 1024
        return f"{kb_size:.1f} KB".replace('.', ',')
    
    elif bytes_size < 1024 * 1024 * 1024:
        mb_size = bytes_size / (1024 * 1024)
        return f"{mb_size:.1f} MB".replace('.', ',')
    
    else:
        gb_size = bytes_size / (1024 * 1024 * 1024)
        return f"{gb_size:.1f} GB".replace('.', ',')