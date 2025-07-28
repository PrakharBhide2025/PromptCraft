# app/services/token_tracker.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
import logging


async def track_token_usage(db: AsyncIOMotorDatabase, llm_call_details: dict):
    try:
        await db.TokenUsageLog.insert_one({
            "prompt_tokens": llm_call_details["prompt_tokens"],
            "completion_tokens": llm_call_details["completion_tokens"],
            "total_tokens": llm_call_details["prompt_tokens"] + llm_call_details["completion_tokens"],
            "model_name": llm_call_details["model_name"],
            "user_id": llm_call_details["user_id"],
            "prompt_id": llm_call_details["prompt_id"],
            "llm_response_log_id": llm_call_details["llm_response_log_id"],
            "timestamp": datetime.utcnow(),
        })
    except Exception as e:
        logging.error(f"token tracker failed: {e}")

