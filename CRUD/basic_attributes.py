
import hashlib
from bson import ObjectId
from fastapi import Depends, HTTPException
import jwt
from pymongo import MongoClient
import os
from dotenv import load_dotenv
# import models.touchscreencms as models
# from redis_client import redis_client
from fastapi.security import OAuth2PasswordBearer

load_dotenv() 

uri = os.getenv('MONGO_URI_VERSION1')

class Attibutes_crud:
    
    def __init__(self):
            self.client = MongoClient(uri)
            self.db = self.client['admin']

    def create(self, collection_name: str, data: dict):
        collection = self.db[collection_name]
        return str(collection.insert_one(data).inserted_id)
    
    def get_all_items(self, collection_name: str) ->list[dict]:
        collection = self.db[collection_name]
        result = list(collection.find({}))
        return result
    
    def get_item_by_attributes_name(self, collection_name:str, product_id: str, item_name:str ):
        collection = self.db[collection_name]
        result = list(collection.find({"_id": product_id}, {item_name:1}))
        return result

    def update_item_by_attributs_name(self, collection_name:str, product_id: str, target_updated_data: dict):
        collection = self.db[collection_name]
    
        update_result = collection.update_one(
            {"_id": product_id},
            {"$set": target_updated_data},
            upsert=False
        )

        if update_result is None or update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="attribute has not been updated")

        return "The attribute has been updated!"

    def read(self, collection_name: str, item_id: str):
        collection = self.db[collection_name]
        return collection.find_one({'_id': ObjectId(item_id)})

    def update(self, collection_name: str, item_id: str, data: dict):
        collection = self.db[collection_name]
        return collection.update_one({'_id': ObjectId(item_id)}, {'$set': data})

    def delete_item_by_attributs_name(self, collection_name:str, product_id: str, target_deleted_data: str):

        collection = self.db[collection_name]
    
        update_result = collection.update_one(
            {"_id": product_id},
            {"$unset": {target_deleted_data: ""}},
            upsert=False
        )
        
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Field has not been removed or product not found")
        
        return "The field has been removed!"

Basic_attributes_crud_instance= Attibutes_crud()
