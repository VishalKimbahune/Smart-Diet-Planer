import os
from pymongo import MongoClient

# Use the environment variable or default to a local MongoDB instance
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")

client = MongoClient(MONGO_URL)
database = client["smart_diet"]

def get_db():
    yield database
