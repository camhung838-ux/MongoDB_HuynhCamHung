import os
from dotenv import load_dotenv
from pymongo import MongoClient


class DbConnect:
    def __init__(self):
        load_dotenv()
        self.mongo_uri = os.getenv("MONGO_URI")
        self.db_name = os.getenv("DB_NAME")

    def aggregate(self, collection_name: str, data: list):
        
        with MongoClient(self.mongo_uri) as client:
            db = client[self.db_name]
            collection = db[collection_name]
            
            with collection.aggregate(data) as cursor:
                return list(cursor)
                
    def insert_one(self, collection_name: str, data: dict):

        with MongoClient(self.mongo_uri) as client:
            db = client[self.db_name]
            collection = db[collection_name]

            with collection.insert_one(data) as cursor:
                return list(cursor)

    def find(self, collection_name: str, query: dict={}, project: dict={}):
         
         with MongoClient(self.mongo_uri) as client:
            db = client[self.db_name]
            collection = db[collection_name]

            with collection.find(query, project) as cursor:
                return list(cursor)
            
    def update_one(self, collection_name: str, query: dict={}, updates: dict={}):

        with MongoClient(self.mongo_uri) as client:
            db = client[self.db_name]
            collection = db[collection_name]

            with collection.update_one(query, updates) as cursor:
                return list(cursor)
            
    def delete_one(self, collection_name: str, query: dict={}):
        
        with MongoClient(self.mongo_uri) as client:
            db = client[self.db_name]
            collection = db[collection_name]

            with collection.delete_one(query) as cursor:
                return list(cursor)


             
