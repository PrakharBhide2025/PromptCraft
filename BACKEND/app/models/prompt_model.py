# app/models/prompt_model.py or app/schemas/prompt.py

from typing import List, Dict, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from app.db.mongo import PyObjectId  # make sure this exists and is correct

class Prompt(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    owner_id: PyObjectId
    name: str
    description: Optional[str]
    tags: List[str] = []
    metadata: Dict[str, Union[str, float]] = {}
    current_version_id: Optional[PyObjectId]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}


class PromptVersion(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    prompt_id: PyObjectId
    version_number: int
    version_name: str
    content: str
    changes_description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
