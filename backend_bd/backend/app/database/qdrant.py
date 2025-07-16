from dotenv import load_dotenv
import os
from qdrant_client import QdrantClient

load_dotenv()  # Carrega variáveis do .env

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

