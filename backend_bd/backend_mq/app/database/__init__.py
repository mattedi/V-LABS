import os

MODO = os.getenv("MODO", "teste")  # padrão: teste

if MODO == "producao":
    from .mongo import (
        db, colecao_usuarios, colecao_perguntas, colecao_respostas,
        colecao_avaliacoes, colecao_logs
    )
else:
    from .mongo_test import (
        db, colecao_usuarios, colecao_avaliacoes, colecao_logs
    )

from .qdrant_client import indexar_documento, buscar_por_texto
