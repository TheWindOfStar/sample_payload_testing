from pydantic import BaseModel, Field
from typing import Dict, List

class UpdateRequest(BaseModel):
    item_id: str 
    fields_to_update: List[str]
    upload_data: list[dict]
