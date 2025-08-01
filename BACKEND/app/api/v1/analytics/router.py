# app/api/v1/analytics/router.py
from fastapi import APIRouter, Depends, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.dependencies import get_db  # Make sure you have this in your project

router = APIRouter(prefix="/analytics", tags=["analytics"])


def admin_guard(request: Request):
    if not getattr(request.state, "is_admin", False):
        raise HTTPException(status_code=403, detail="Admin credentials required")


@router.get("/prompt-usage")
async def prompt_usage(request: Request, db: AsyncIOMotorDatabase = Depends(get_db)):
    admin_guard(request)
    pipeline = [
        {"$group": {"_id": "$prompt_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top = await db.LLMResponseLog.aggregate(pipeline).to_list(length=10)
    total_calls = await db.LLMResponseLog.estimated_document_count()
    return {
        "total_llm_calls": total_calls,
        "top_prompts": top
    }


@router.get("/evaluation-trends")
async def evaluation_trends(request: Request, db: AsyncIOMotorDatabase = Depends(get_db)):
    admin_guard(request)
    # Placeholder for future logic
    return {
        "average_scores": {},
        "score_distribution": {}
    }


@router.get("/token-usage")
async def token_usage(request: Request, db: AsyncIOMotorDatabase = Depends(get_db)):
    admin_guard(request)
    per_model = await db.TokenUsageLog.aggregate([
        {"$group": {"_id": "$model_name", "total": {"$sum": "$total_tokens"}}}
    ]).to_list(length=10)

    per_user = await db.TokenUsageLog.aggregate([
        {"$group": {"_id": "$user_id", "total": {"$sum": "$total_tokens"}}}
    ]).to_list(length=10)

    return {
        "total_tokens_per_model": per_model,
        "total_tokens_per_user": per_user
    }
