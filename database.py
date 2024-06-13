from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")


db = client.admin

collection_name = db["sample_payload_collection"]
