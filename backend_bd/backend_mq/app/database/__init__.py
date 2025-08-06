import os

MODO = os.getenv("MODO", "teste")  # padrão: teste
print(f"🔧 Modo database: {MODO}")

try:
    if MODO == "producao":
        print("📚 Carregando database de produção...")
        from .mongo import (
            db, colecao_usuarios, colecao_perguntas, colecao_respostas,
            colecao_avaliacoes, colecao_logs, colecao_embeddings, colecao_interacoes,
            colecao_alunos, colecao_sessoes, colecao_configuracoes, 
            colecao_modos_entrada, colecao_logs_interacao
        )
    else:
        print("🧪 Carregando database de teste...")
        from .mongo_test import (
            db, colecao_usuarios, colecao_avaliacoes, colecao_logs
        )
        
        # Criar coleções faltantes para compatibilidade
        colecao_perguntas = getattr(db, 'perguntas', None) if db else None
        colecao_respostas = getattr(db, 'respostas', None) if db else None
        colecao_embeddings = getattr(db, 'embeddings', None) if db else None
        colecao_interacoes = getattr(db, 'interacoes', None) if db else None
        colecao_alunos = getattr(db, 'alunos', None) if db else None
        colecao_sessoes = getattr(db, 'sessoes', None) if db else None
        colecao_configuracoes = getattr(db, 'configuracoes', None) if db else None
        colecao_modos_entrada = getattr(db, 'modos_entrada', None) if db else None
        colecao_logs_interacao = getattr(db, 'logs_interacao', None) if db else None
    
    print("✅ Database inicializado com sucesso")
    
except ImportError as e:
    print(f"⚠️ Erro ao importar database: {e}")
    print("🔄 Usando fallback - variáveis None")
    
    # Fallback completo - todas as variáveis como None
    db = None
    colecao_usuarios = None
    colecao_perguntas = None
    colecao_respostas = None
    colecao_avaliacoes = None
    colecao_logs = None
    colecao_embeddings = None
    colecao_interacoes = None
    colecao_alunos = None
    colecao_sessoes = None
    colecao_configuracoes = None
    colecao_modos_entrada = None
    colecao_logs_interacao = None

# Imports adicionais se existirem
try:
    from .qdrant_client import indexar_documento, buscar_por_texto
    print("✅ Qdrant client carregado")
except ImportError:
    print("⚠️ Qdrant client não disponível")
    indexar_documento = None
    buscar_por_texto = None

# Exports para facilitar imports
__all__ = [
    'db',
    'colecao_usuarios', 'colecao_perguntas', 'colecao_respostas', 
    'colecao_avaliacoes', 'colecao_logs', 'colecao_embeddings',
    'colecao_interacoes', 'colecao_alunos', 'colecao_sessoes',
    'colecao_configuracoes', 'colecao_modos_entrada', 'colecao_logs_interacao',
    'indexar_documento', 'buscar_por_texto'
]