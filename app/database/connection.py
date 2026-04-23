import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class Database:
    client = None
    db = None

    @classmethod
    def connect(cls):
        if cls.client is None:
            cls.client = MongoClient(os.getenv("MONGODB_URI"))
            cls.db = cls.client[os.getenv("DATABASE_NAME")]
            print("Connected to MongoDB - RIMS Cluster")
        return cls.db