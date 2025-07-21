import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://mattediVibe:vibe1234@vibe-learning.vndvwiu.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = os.getenv("DATABASE_NAME", "vibe_learning")

try:
    client = MongoClient(MONGODB_URI)
    client.admin.command('ping')
    print("✅ MongoDB conectado")
    db = client[DATABASE_NAME]
    colecao_usuarios = db["usuarios"]
    colecao_avaliacoes = db["avaliacoes"]
    colecao_logs = db["logs"]
except Exception as e:
    print(f"❌ Erro MongoDB: {e}")
    raise e
