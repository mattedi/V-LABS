# Conexão MongoDB
from pymongo import MongoClient

client = MongoClient("mongodb+srv://usuario:senha@cluster.mongodb.net")
db = client["vibe_learning"]
