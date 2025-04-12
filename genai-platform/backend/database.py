# backend/database.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["genai-platform"]

def get_user_collection():
    return db["users"]

async def get_tenant_collection(tenant_id: str, collection_name: str):
    db = get_database()
    return db[f"{tenant_id}_{collection_name}"]

def get_chat_collection():
    return db["chat_messages"]

