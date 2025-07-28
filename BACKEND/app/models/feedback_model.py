# FIX ME: Stub or import missing for one or more symbols like 'PyObjectId', 'users_collection'
from pydantic import BaseModel, Field
from app.models.common import PyObjectId


class FeedbackModel(BaseModel):
    id: PyObjectId = await Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    message: str
    rating: int
    created_at: str
