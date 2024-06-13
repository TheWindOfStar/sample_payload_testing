from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Router.basic_attributes import router as basic_attribute_router
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('MONGO_URI_VERSION1')

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(basic_attribute_router)

@app.get("/")
def read_root():
    return "Welcome to unfold solution - sample_payload - Backend"