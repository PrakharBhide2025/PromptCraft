from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List
from app.dependencies import get_current_user
from app.services.prompt_service import create_prompt  # + other functions
from app.api.v1.prompts.schemas import PromptCreate, PromptResponse

router = APIRouter(prefix="/prompts", tags=["prompts"])

@router.post("/", response_model=PromptResponse)
async def create_endpoint(data: PromptCreate, user=Depends(get_current_user)):
    return await create_prompt(user["_id"], data)
