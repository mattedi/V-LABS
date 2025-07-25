"""
Executar servidor de desenvolvimento.
Arquivo simplificado para evitar problemas de import.
"""

import uvicorn
import sys
import os

# Adiciona diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 V-LABS Backend Communication")
    print("📍 http://localhost:8000")
    print("📚 http://localhost:8000/docs")
    print("🏥 http://localhost:8000/health")
    print("-" * 40)
    
    try:
        # Tenta importar para verificar se tudo está OK
        import config
        print("✅ Config carregado")
        
        import routers
        print("✅ Routers carregados")
        
        import utils
        print("✅ Utils carregados")
        
        print("✅ Iniciando servidor...")
        
        # Inicia o servidor
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        print("💡 Executando apenas uvicorn...")
        
        # Fallback: executa uvicorn diretamente
        os.system("uvicorn main:app --reload --host 127.0.0.1 --port 8000")