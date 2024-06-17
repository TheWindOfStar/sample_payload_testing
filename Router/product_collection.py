import json
import random
import string
from lxml import html
import os
from fastapi import APIRouter, Depends, File, HTTPException, Body, UploadFile, requests
from pymongo import MongoClient
from Operations.product_collection import Product_crud_instance
from datetime import datetime, timedelta, timezone, time
import jwt
from dotenv import load_dotenv
import httpx
import pytz
import csv
from io import StringIO

router = APIRouter()

load_dotenv() 

uri = os.getenv('MONGO_URI_VERSION1')

client = MongoClient(uri)
db = client['admin']

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
    if file.content_type == "application/json":
        try:
            items = json.loads(data)  # Assume JSON file contains a list of items
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=422, detail=f"JSON decoding error at line {e.lineno}, column {e.colno}: {e.msg}")
    elif file.content_type == "text/csv":
        try:
            data_str = data.decode('utf-8')
            csv_reader = csv.DictReader(StringIO(data_str))
            items = [row for row in csv_reader]
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"CSV decoding error: {str(e)}")

    results = []
    for item in items:
        result = Product_crud_instance.validate_json_and_csv_item(item)
        results.append(result)
    
    return results