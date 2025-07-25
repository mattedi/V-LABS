"""
Arquivo de inicialização simplificado para teste.
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 Iniciando V-LABS Backend Communication...")
    print("📍 URL: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("🏥 Health: http://localhost:8000/health")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )