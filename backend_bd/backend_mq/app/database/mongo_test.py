from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DATABASE")

client = MongoClient(MONGO_URI)

try:
    db = client[DB_NAME]
    print("✅ MongoDB conectado:", db.list_collection_names())
except Exception as e:
    print("❌ Erro ao conectar no MongoDB:", e)
