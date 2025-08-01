# app/api/v1/feedback/router.py

from fastapi import APIRouter, Depends, Request, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from app.schemas.feedback import *
from app.dependencies import get_mongo_db  # make sure this exists

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("/submit", response_model=FeedbackResponse)
async def submit_feedback(
    req: FeedbackCreate,
    request: Request,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    user_id = request.state.user_id

    # Check if LLM response exists
    llm_response = await db.LLMResponseLog.find_one({"_id": ObjectId(req.llm_response_log_id)})
    if not llm_response:
        raise HTTPException(status_code=404, detail="LLM response not found")

    # Construct feedback document
    doc = {
        "llm_response_log_id": ObjectId(req.llm_response_log_id),
        "user_id": ObjectId(user_id),
        "rating": req.rating,
        "comment": req.comment,
        "timestamp": datetime.utcnow()
    }

    # Insert into UserFeedback collection
    result = await db.UserFeedback.insert_one(doc)

    # Return response
    return FeedbackResponse(
        feedback_id=str(result.inserted_id),
        llm_response_log_id=req.llm_response_log_id,
        user_id=user_id,
        rating=req.rating,
        comment=req.comment,
        timestamp=doc["timestamp"]
    )
