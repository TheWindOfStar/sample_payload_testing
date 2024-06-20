
from datetime import datetime
import hashlib
import json
from bson import ObjectId
from fastapi import Depends, HTTPException
import jwt
from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from pymongo import MongoClient
from bson import ObjectId
from pymongo import ReturnDocument
import copy

load_dotenv() 

uri = os.getenv('MONGO_URI_VERSION1')

class Attibutes_crud:
    
    def __init__(self):
            self.client = MongoClient(uri)
            self.db = self.client['UnfoldSolutionIntership']

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
            return item
        
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid JSON: {str(e)}")



    def csv_to_json(self, csv_content):
        # Convert the CSV string to a DataFrame
        df = pd.read_csv(pd.compat.StringIO(csv_content))
        
        # Convert the DataFrame to a JSON string
        json_result = df.to_json(orient='records')
        
        # Convert the JSON string to a list of dictionaries
        json_data = json.loads(json_result)
        
        return json_data

    def deep_compare_dicts(self, orig_dict, new_dict, results, parent_key=''):
        for key in new_dict:
            full_key = f"{parent_key}.{key}" if parent_key else key
            if key not in orig_dict:
                results.append({full_key: {'before': None, 'after': new_dict[key]}})
            elif isinstance(new_dict[key], dict) and isinstance(orig_dict[key], dict):
                self.deep_compare_dicts(orig_dict[key], new_dict[key], results, full_key)
            elif isinstance(new_dict[key], list) and isinstance(orig_dict[key], list):
                self.compare_lists(orig_dict[key], new_dict[key], results, full_key)
            elif new_dict[key] != orig_dict[key]:
                results.append({full_key: {'before': orig_dict[key], 'after': new_dict[key]}})

    def compare_lists(self, orig_list, new_list, results, parent_key):
        for index, items in enumerate(zip(orig_list, new_list)):
            orig_item, new_item = items
            item_key = f"{parent_key}[{index}]"
            if isinstance(orig_item, dict) and isinstance(new_item, dict):
                self.deep_compare_dicts(orig_item, new_item, results, item_key)
            elif orig_item != new_item:
                results.append({item_key: {'before': orig_item, 'after': new_item}})
        # Handle size differences
        if len(orig_list) != len(new_list):
            results.append({parent_key: {'before': 'List size ' + str(len(orig_list)), 'after': 'List size ' + str(len(new_list))}})

    def compare_data(self, collection_name: str, item_id, updated_data):
        collection = self.db[collection_name]
        original_document = collection.find_one({"_id": item_id})

        if not original_document:
            return {"_id": item_id, "error": "Document not found"}

        comparison_results = []
        self.deep_compare_dicts(original_document, updated_data, comparison_results)

        return {"_id": item_id, "comparisons": comparison_results}


    def update_selected_fields(self, collection_name, item_id, update_data, fields_to_update):
        collection = self.db[collection_name]
        update_subset = {f"{key}": update_data[key] for key in fields_to_update if key in update_data}

        if not update_subset:
            return None

        update_operation = {"$set": update_subset}

        updated_document = collection.find_one_and_update(
            {"_id": item_id},
            update_operation,
            return_document=ReturnDocument.AFTER
        )

        # Assuming record_update is a method that logs or handles the update
        self.record_update(item_id, update_subset)

        return updated_document

    def record_update(self, item_id, update_subset):
        # Log the update or perform additional actions
        print(f"Update recorded for {item_id} with changes: {update_subset}")


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
