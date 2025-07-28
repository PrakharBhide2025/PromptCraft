from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId


class Prompt(Document):
    title: str
    content: str
    owner_id: ObjectId
    tags: Optional[List[str]] = []
    versions: Optional[List[dict]] = []
    created_at: Optional[str]
    updated_at: Optional[str]

    # 🔥 New fields for analytics
    views: int = 0
    edits: int = 0
    eval_count: int = 0

    class Settings:
        name = "prompts"
