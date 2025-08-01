# app/api/v1/evaluation/router.py

from fastapi import APIRouter, Depends, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime

from app.schemas.evaluation import *
from app.services.evaluation_service import EvaluationService
from app.dependencies import get_mongo_db  # assuming it's defined

router = APIRouter(prefix="/evaluation", tags=["evaluation"])
eval_svc = EvaluationService()


@router.post("/run", response_model=EvaluationResultResponse)
async def run_evaluation(
    req: EvaluationRequest,
    request: Request,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    doc = await db.LLMResponseLog.find_one({"_id": ObjectId(req.llm_response_log_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="LLM response not found")

    scores = await eval_svc.evaluate_response(
        doc["generated_output"],
        doc["input_prompt_content"],
        req.metrics
    )

    eval_doc = {
        "llm_response_log_id": doc["_id"],
        "evaluator_user_id": ObjectId(request.state.user_id),
        "scores": scores,
        "evaluation_timestamp": datetime.utcnow()
    }

    await db.PromptEvaluation.insert_one(eval_doc)

    return EvaluationResultResponse(
        llm_response_log_id=req.llm_response_log_id,
        scores=scores
    )


@router.post("/compare", response_model=LLMComparisonResponse)
async def compare(
    req: LLMComparisonRequest,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    doc1 = await db.LLMResponseLog.find_one({"_id": ObjectId(req.llm_response_log_id_1)})
    doc2 = await db.LLMResponseLog.find_one({"_id": ObjectId(req.llm_response_log_id_2)})

    if not doc1 or not doc2:
        raise HTTPException(status_code=404, detail="One or both responses not found")

    comp = await eval_svc.compare_llm_outputs(
        doc1["generated_output"],
        doc2["generated_output"],
        req.comparison_criteria
    )

    return LLMComparisonResponse(
        llm_response_log_id_1=req.llm_response_log_id_1,
        llm_response_log_id_2=req.llm_response_log_id_2,
        comparison_results=comp
    )
