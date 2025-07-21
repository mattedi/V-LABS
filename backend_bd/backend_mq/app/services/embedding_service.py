from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer("all-MiniLM-L6-v2")

def gerar_vetor(texto: str) -> list[float]:
    return modelo.encode(texto).tolist()
