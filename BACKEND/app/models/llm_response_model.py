# FIX ME: Stub or import missing for one or more symbols like 'PyObjectId', 'users_collection'
from pydantic import BaseModel, Field
from app.models.common import PyObjectId


class LLMResponseModel(BaseModel):
    id: PyObjectId = await Field(default_factory=PyObjectId, alias="_id")
    prompt_id: str
    llm_response: str
    model_used: str
    created_at: str
