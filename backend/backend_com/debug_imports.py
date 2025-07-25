"""
Script para diagnosticar problemas de importação do utils.

Execute este arquivo para identificar exatamente qual é o problema
com os imports do pacote utils.
"""

import os
import sys
import traceback

def diagnosticar_imports():
    """Diagnostica problemas de importação step by step."""
    
    print("🔍 DIAGNÓSTICO DE IMPORTS DO UTILS")
    print("=" * 50)
    
    # 1. Verifica estrutura de arquivos
    print("\n1. VERIFICANDO ESTRUTURA DE ARQUIVOS:")
    
    utils_dir = "utils"
    arquivos_esperados = [
        "__init__.py",
        "logging.py", 
        "helpers.py",
        "formatters.py",
        "security.py",
        "validators.py"
    ]
    
    if os.path.exists(utils_dir):
        print(f"✅ Diretório {utils_dir}/ existe")
        
        for arquivo in arquivos_esperados:
            caminho = os.path.join(utils_dir, arquivo)
            if os.path.exists(caminho):
                print(f"✅ {arquivo} existe")
            else:
                print(f"❌ {arquivo} NÃO EXISTE")
    else:
        print(f"❌ Diretório {utils_dir}/ NÃO EXISTE")
        return
    
    # 2. Verifica conteúdo do __init__.py
    print("\n2. VERIFICANDO __init__.py:")
    
    try:
        with open(os.path.join(utils_dir, "__init__.py"), 'r', encoding='utf-8') as f:
            conteudo = f.read()
            
        if "from .logging import" in conteudo:
            print("✅ __init__.py contém import de .logging")
        else:
            print("❌ __init__.py NÃO contém import de .logging")
            
        if "setup_logger" in conteudo:
            print("✅ setup_logger está no __init__.py")
        else:
            print("❌ setup_logger NÃO está no __init__.py")
            
        if "configure_structured_logging" in conteudo:
            print("✅ configure_structured_logging está no __init__.py")
        else:
            print("❌ configure_structured_logging NÃO está no __init__.py")
            
    except Exception as e:
        print(f"❌ Erro ao ler __init__.py: {e}")
    
    # 3. Testa imports um por um
    print("\n3. TESTANDO IMPORTS:")
    
    # Teste 1: Import do pacote utils
    print("\nTeste 1: from utils import setup_logger, configure_structured_logging")
    try:
        from utils import setup_logger, configure_structured_logging
        print("✅ SUCESSO - Import do pacote utils funcionou")
        
        # Testa se as funções funcionam
        try:
            configure_structured_logging()
            logger = setup_logger("teste")
            logger.info("Teste de logging")
            print("✅ Funções funcionam corretamente")
        except Exception as e:
            print(f"❌ Erro ao executar funções: {e}")
            
    except Exception as e:
        print(f"❌ FALHA: {e}")
        print(f"Traceback: {traceback.format_exc()}")
    
    # Teste 2: Import direto do módulo
    print("\nTeste 2: from utils.logging import setup_logger, configure_structured_logging")
    try:
        from utils.logging import setup_logger, configure_structured_logging
        print("✅ SUCESSO - Import direto do módulo funcionou")
    except Exception as e:
        print(f"❌ FALHA: {e}")
    
    # Teste 3: Import do módulo inteiro
    print("\nTeste 3: import utils.logging")
    try:
        import utils.logging
        print("✅ SUCESSO - Import do módulo inteiro funcionou")
        
        if hasattr(utils.logging, 'setup_logger'):
            print("✅ setup_logger está disponível")
        else:
            print("❌ setup_logger NÃO está disponível")
            
        if hasattr(utils.logging, 'configure_structured_logging'):
            print("✅ configure_structured_logging está disponível")
        else:
            print("❌ configure_structured_logging NÃO está disponível")
            
    except Exception as e:
        print(f"❌ FALHA: {e}")
    
    # 4. Verifica Python path
    print("\n4. VERIFICANDO PYTHON PATH:")
    print(f"Diretório atual: {os.getcwd()}")
    print("Python path:")
    for i, path in enumerate(sys.path):
        print(f"  {i}: {path}")
    
    # 5. Verifica se logging.py tem sintaxe válida
    print("\n5. VERIFICANDO SINTAXE DO logging.py:")
    try:
        with open(os.path.join(utils_dir, "logging.py"), 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        # Tenta compilar o código
        compile(codigo, "logging.py", "exec")
        print("✅ Sintaxe do logging.py está correta")
        
        # Verifica se as funções estão definidas
        if "def setup_logger" in codigo:
            print("✅ setup_logger está definida")
        else:
            print("❌ setup_logger NÃO está definida")
            
        if "def configure_structured_logging" in codigo:
            print("✅ configure_structured_logging está definida")
        else:
            print("❌ configure_structured_logging NÃO está definida")
            
    except SyntaxError as e:
        print(f"❌ ERRO DE SINTAXE no logging.py: {e}")
    except Exception as e:
        print(f"❌ Erro ao verificar logging.py: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 DIAGNÓSTICO CONCLUÍDO")


if __name__ == "__main__":
    diagnosticar_imports()