from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId


class PromptOut(BaseModel):
    id: str
    title: str
    content: str
    tags: List[str]
    owner_id: str
    views: int
    edits: int
    eval_count: int

    class Config:
        orm_mode = True
