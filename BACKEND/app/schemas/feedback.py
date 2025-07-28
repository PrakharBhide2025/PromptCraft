from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FeedbackCreate(BaseModel):
    llm_response_log_id: str
    rating: int
    comment: Optional[str] = None


class FeedbackResponse(BaseModel):
    feedback_id: str
    llm_response_log_id: str
    user_id: str
    rating: int
    comment: Optional[str]
    timestamp: datetime
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FeedbackCreate(BaseModel):
    llm_response_log_id: str = Field(..., description="ID of the LLM response to which feedback is linked")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: Optional[str] = Field(None, description="Optional comment provided by the user")


class FeedbackResponse(BaseModel):
    feedback_id: str
    llm_response_log_id: str
    user_id: str
    rating: int
    comment: Optional[str]
    timestamp: datetime

