# Embedding service - versão mock para desenvolvimento rápido
import numpy as np
import random

def gerar_vetor(texto: str) -> list:
    """Gera vetor mock para desenvolvimento - compatível com sentence-transformers."""
    # Mock vector de 384 dimensões (padrão do all-MiniLM-L6-v2)
    np.random.seed(hash(texto) % 2**32)  # Determinístico baseado no texto
    return np.random.rand(384).tolist()

def buscar_similares(vetor: list, limite: int = 5) -> list:
    """Busca mock para desenvolvimento."""
    mock_results = []
    for i in range(min(limite, 3)):
        mock_results.append({
            "id": f"mock_doc_{i}",
            "score": random.uniform(0.7, 0.95),
            "texto": f"Documento similar mock {i+1}",
            "metadata": {"tipo": "mock"}
        })
    return mock_results

class MockSentenceTransformer:
    """Mock da classe SentenceTransformer."""
    def __init__(self, model_name: str = "mock"):
        self.model_name = model_name
        
    def encode(self, texts, **kwargs):
        """Mock do método encode."""
        if isinstance(texts, str):
            return gerar_vetor(texts)
        return [gerar_vetor(text) for text in texts]

print("⚠️ Usando embedding service MOCK - sentence_transformers não instalado")
print("✅ Para produção, instale: pip install sentence-transformers")
