import random
import string
from lxml import html
import os
from fastapi import APIRouter, Depends, HTTPException, Body, requests
from pymongo import MongoClient
from Operations.product_collection import Product_crud_instance
from datetime import datetime, timedelta, timezone, time
import jwt
from dotenv import load_dotenv
import httpx
import pytz
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