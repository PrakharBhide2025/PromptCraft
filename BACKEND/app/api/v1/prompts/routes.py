# # app/api/v1/prompts/routes.py

# from fastapi import APIRouter, Request, HTTPException, Depends
# from pydantic import BaseModel

# router = APIRouter()

# class PromptSchema(BaseModel):
#     input_text: str
#     purpose: str

# @router.post("/")
# async def create_prompt(prompt: PromptSchema, request: Request):
#     user_id = request.state.user_id  # Comes from middleware
#     if not user_id:
#         raise HTTPException(status_code=401, detail="Unauthorized")
    
#     return {
#         "message": "Prompt received",
#         "user_id": user_id,
#         "prompt": prompt.dict()
#     }

# app/api/v1/prompts/routes.py

# from fastapi import APIRouter, Request, HTTPException
# from app.schemas.prompt_schema import PromptSchema

# router = APIRouter()


# # Schema is now shared between both routes (imported from schemas)
# # class PromptSchema(BaseModel):
# #     input_text: str
# #     purpose: str
# #     name: Optional[str] = None
# #     description: Optional[str] = None
# #     tags: List[str] = []
# #     prompt_metadata: Dict[str, Any] = {}


# # ✅ Route 1: Create a new prompt
# @router.post("/")
# async def create_prompt(prompt: PromptSchema, request: Request):
#     user_id = request.state.user_id  # Comes from middleware
#     if not user_id:
#         raise HTTPException(status_code=401, detail="Unauthorized")
    
#     # Save prompt logic here (e.g., insert to MongoDB)
#     return {
#         "message": "New prompt created",
#         "user_id": user_id,
#         "prompt": prompt.dict()
#     }


# # ✅ Route 2: Save a version of an existing prompt
# @router.post("/{prompt_id}/versions")
# async def save_prompt_version(prompt_id: str, prompt: PromptSchema, request: Request):
#     user_id = request.state.user_id  # Comes from middleware
#     if not user_id:
#         raise HTTPException(status_code=401, detail="Unauthorized")

#     # Save version logic here (e.g., insert into versions collection)

#     return {
#         "message": f"Version saved for prompt ID: {prompt_id}",
#         "user_id": user_id,
#         "version_data": prompt.dict()
#     }

from fastapi import APIRouter, Request, HTTPException, Depends
from app.schemas.prompt_schema import PromptSchema
from app.db.mongo import get_database  # ✅
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def create_prompt(prompt: PromptSchema, request: Request, db=Depends(get_database)):
    user_id = request.state.user_id
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    prompt_data = prompt.dict()
    prompt_data["user_id"] = user_id

    result = await db["prompts"].insert_one(prompt_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to create prompt")

    return {
        "id": str(result.inserted_id),   # ✅ This is what frontend expects
        "message": "New prompt created",
    }
