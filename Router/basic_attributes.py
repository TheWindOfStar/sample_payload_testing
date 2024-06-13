import random
import string
from lxml import html
import os
from fastapi import APIRouter, Depends, HTTPException, Body, requests
from pymongo import MongoClient
from CRUD.basic_attributes import Basic_attributes_crud_instance
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

@router.get("/GetAllItems")
def get_all_items():
    result = Basic_attributes_crud_instance.get_all_items("sample_payload_collection")
    return result

@router.get("/GetItemByName/{ProductId}/subname/{item_name}")
def get_all_items(ProductId:str, item_name: str):
    result = Basic_attributes_crud_instance.get_item_by_attributes_name("sample_payload_collection", ProductId, item_name)
    return result

@router.put("/UpdateAttributeWithProductId/{ProductId}")
def update_item_by_attributs_name(ProductId: str, Updated_data:dict):
    result = Basic_attributes_crud_instance.update_item_by_attributs_name("sample_payload_collection", ProductId, Updated_data)
    return result

@router.delete("/DeleteAttributeWithProductId/{ProductId}")
def delete_item_by_attributs_name(ProductId: str, Deleted_data:str):
    result = Basic_attributes_crud_instance.delete_item_by_attributs_name("sample_payload_collection", ProductId, Deleted_data)
    return result