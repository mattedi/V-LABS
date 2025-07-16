# Conexão MongoDB
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()


client = MongoClient("mongodb+srv://mattediVibe:vibe1234@vibe-learning.vndvwiu.mongodb.net/?retryWrites=true&w=majority")
db = client["vibe_learning"]
