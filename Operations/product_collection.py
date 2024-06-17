
import hashlib
import json
from bson import ObjectId
from fastapi import Depends, HTTPException
import jwt
from pymongo import MongoClient
import os
from dotenv import load_dotenv
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
    
    def get_item_by_product_id(self, collection_name: str, product_id:str) ->list[dict]:
        collection = self.db[collection_name]
        result = list(collection.find({"_id": product_id}))
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
    

    def upload_file_and_check_format(self, collection_name:str, product_id: str, target_updated_data: dict):
        
        
        
        
        return True

    def validate_json_and_csv_item(self, item: dict) -> dict:

        errors =[]
        try: 
            item_id = item.get("_id", None)
            if not item_id or not isinstance(item_id, str):
                errors.append({"id": item_id, "status": "invalid", "error": "Missing or invalid _id"})

            if not isinstance(item.get("_keywords", []), list):
                errors.append({"id": item_id, "status": "invalid", "error": "_keywords must be a list"})
            
            if not isinstance(item.get("additives_tags", []), list):
                errors.append({"id": item_id, "status": "invalid", "error": "additives_tags must be a list"})
            
            if not isinstance(item.get("additives_n", 0), int):
                errors.append({"id": item_id, "status": "invalid", "error": "additives_n must be an integer"})

            if errors:
                return {"id": item_id, "errors": errors}
            return {"id": item_id, "status": "valid"}
        
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid JSON: {str(e)}")


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

Product_crud_instance= Attibutes_crud()
