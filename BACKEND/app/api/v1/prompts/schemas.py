from typing import Optional, List, Dict, Union
from pydantic import BaseModel, Field
from datetime import datetime


class PromptVersionResponse(BaseModel):
    id: str
    prompt_id: str
    version_number: int
    version_name: str
    content: str
    changes_description: Optional[str] = None
    created_at: datetime


class PromptCreate(BaseModel):
    name: str = Field(..., min_length=1, example="Greeting Prompt")
    description: Optional[str] = Field(None, example="Used to greet users.")
    content: str = Field(..., min_length=10, example="Hello, my name is {{name}}.")
    tags: Optional[List[str]] = []
    prompt_metadata: Optional[Dict[str, Union[float, str]]] = None


class PromptUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str]
    tags: Optional[List[str]]
    prompt_metadata: Optional[Dict[str, Union[float, str]]]


class PromptResponse(BaseModel):
    id: str
    owner_id: str
    name: str
    description: Optional[str]
    tags: List[str]
    prompt_metadata: Optional[Dict[str, Union[float, str]]]
    current_version_id: str
    created_at: datetime
    updated_at: datetime
    current_version: PromptVersionResponse


class PromptListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    prompts: List[PromptResponse]
