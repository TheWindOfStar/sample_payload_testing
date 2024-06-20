import json
import random
import string
from typing import List
from lxml import html
import os
from fastapi import APIRouter, Depends, File, Form, HTTPException, Body, UploadFile, requests
import pandas as pd
from pymongo import MongoClient
from Operations.product_collection import Product_crud_instance
from datetime import datetime, timedelta, timezone, time
import schemas as schemas
import jwt
from dotenv import load_dotenv
import httpx
import pytz
import csv
from io import StringIO
from fastapi import HTTPException

router = APIRouter()

load_dotenv() 

uri = os.getenv('MONGO_URI_VERSION1')

client = MongoClient(uri)
db = client['UnfoldSolutionIntership']

@router.get("/GetItemById/{ProductId}")
def get_all_items(ProductId:str):
    result = Product_crud_instance.get_item_by_product_id("sample_payload_collection", ProductId)
    return result

@router.get("/GetAttriByName/{ProductId}/AttriName/{attri_name}")
def get_all_items(ProductId:str, attri_name: str):
    result = Product_crud_instance.get_item_by_attributes_name("sample_payload_collection", ProductId, attri_name)
    return result

@router.put("/UpdateAttributeWithProductId/{ProductId}")
def update_item_by_attributs_name(ProductId: str, Updated_data:dict):
    result = Product_crud_instance.update_item_by_attributs_name("sample_payload_collection", ProductId, Updated_data)
    return result

@router.delete("/DeleteAttributeWithProductId/{ProductId}")
def delete_item_by_attributs_name(ProductId: str, Deleted_data:str):
    result = Product_crud_instance.delete_item_by_attributs_name("sample_payload_collection", ProductId, Deleted_data)
    return result

@router.post("/UploadFileWithFormatCheck")
async def create_upload_file(file: UploadFile = File(...)):
    
    if file.content_type not in ["application/json", "text/csv"]:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    data = await file.read()
    results = []

    if file.content_type == "application/json":
        try:
            items = json.loads(data)  # Assume JSON file contains a list of items
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=422, detail=f"JSON decoding error at line {e.lineno}, column {e.colno}: {e.msg}")
        
        for item in items:
            result = Product_crud_instance.validate_json_and_csv_item(item)
            results.append(result)
    
    
    elif file.content_type == "text/csv":
        try:
            data_str = data.decode('utf-8')
            csv_reader = csv.DictReader(StringIO(data_str))
            items = [row for row in csv_reader]
            result = Product_crud_instance.csv_to_json(data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"CSV decoding error: {str(e)}")
        
        return result
    
    return results

@router.post("/ComparisonDataSets")
async def comparison_dataset(file: UploadFile = File(...)):
    data = await file.read()
    items = json.loads(data)
    final_result = []
    for item in items:
        item_id = item.get("_id", None)
        result = Product_crud_instance.compare_data("sample_payload_collection", item_id, item)
        final_result.append(result)
    return final_result


@router.post("/UpdateSelectedFields")
async def update_selected_fields(update_request_data: schemas.UpdateRequest):
    try:

        # update_data = json.loads(await file.read())
        item_id = update_request_data.item_id
        print(item_id)
        fields_to_update_list = update_request_data.fields_to_update
        print(fields_to_update_list)
        upload_data = update_request_data.upload_data
        
        for each_item in upload_data:
            if each_item.get("_id") == item_id:
                target_upload_data = each_item
        
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(target_upload_data)

        updated_document = Product_crud_instance.update_selected_fields(
            "sample_payload_collection",
            item_id,
            target_upload_data,
            fields_to_update_list
        )

        if not updated_document:
            raise HTTPException(status_code=404, detail="Document not found")

        return {"updated": True, "document": updated_document}

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=422, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
