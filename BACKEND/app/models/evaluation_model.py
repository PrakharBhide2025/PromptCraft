# FIX ME: Stub or import missing for one or more symbols like 'PyObjectId', 'users_collection'
from pydantic import BaseModel, Field
from app.models.common import PyObjectId


class EvaluationModel(BaseModel):
    id: PyObjectId = await Field(default_factory=PyObjectId, alias="_id")
    prompt_id: str
    score: float
    comments: str
    created_at: str
