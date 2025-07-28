# import logging
# from typing import Optional, List, Dict
# from datetime import datetime
# from motor.motor_asyncio import AsyncIOMotorDatabase
# from app.models.prompt_model import Prompt, PromptVersion
# from app.api.v1.prompts.schemas import PromptCreate, PromptUpdate, PromptVersionResponse, PromptResponse

# logger = logging getLogger(__name__)


# async def create_prompt(db: AsyncIOMotorDatabase, owner_id, data: PromptCreate) -> PromptResponse:
#     # create prompt + initial version atomically
#     prompt = Prompt(owner_id=owner_id, name=data.name, description=data.description,
#                     tags=data.tags or [], metadata=data.metadata or {},
#                     current_version_id=None)
#     res = await db.prompts insert_one(prompt.dict(by_alias=True)
#     prompt.id=res.inserted_id

#     version=PromptVersion(prompt_id=prompt.id, version_number=1,
#                             version_name="v1", content=data.content,
#                             changes_description="Initial version")
#     resv=await db.prompt_versions insert_one(version.dict(by_alias=True)
#     version.id=resv.inserted_id

#     # update prompt current_version_id
#     await db.prompts update_one({'_id': prompt.id}, {'$set': {'current_version_id': version.id, 'updated_at': datetime.utcnow()
#     prompt.current_version_id = version.id
#     logger info(f"Prompt {prompt.id} created by {owner_id}")

#     return PromptResponse(
#         id=str(prompt.id),
#         owner_id=str(owner_id),
#         name=prompt.name,
#         description=prompt.description,
#         tags=prompt.tags,
#         metadata=prompt.metadata,
#         current_version_id=str(version.id),
#         created_at=prompt.created_at,
#         updated_at=prompt.updated_at,
#         current_version=PromptVersionResponse(
#             id=str(version.id),
#             prompt_id=str(prompt.id),
#             version_number=version.version_number,
#             version_name=version.version_name,
#             content=version.content,
#             changes_description=version.changes_description,
#             created_at=version.created_at
#         )
#     )

import logging
from typing import Optional, List, Dict
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.prompt_model import Prompt, PromptVersion
from app.api.v1.prompts.schemas import PromptCreate, PromptUpdate, PromptVersionResponse, PromptResponse

logger = logging.getLogger(__name__)

async def create_prompt(db: AsyncIOMotorDatabase, owner_id, data: PromptCreate) -> PromptResponse:
    # Step 1: Create base prompt document
    prompt = Prompt(
        owner_id=owner_id,
        name=data.name,
        description=data.description,
        tags=data.tags or [],
        metadata=data.prompt_metadata or {},
        current_version_id=None
    )

    res = await db.prompts.insert_one(prompt.dict(by_alias=True))
    prompt.id = res.inserted_id

    # Step 2: Create initial version of the prompt
    version = PromptVersion(
        prompt_id=prompt.id,
        version_number=1,
        version_name="v1",
        content=data.content,
        changes_description="Initial version"
    )

    resv = await db.prompt_versions.insert_one(version.dict(by_alias=True))
    version.id = resv.inserted_id

    # Step 3: Update current_version_id in prompt
    await db.prompts.update_one(
        {'_id': prompt.id},
        {'$set': {'current_version_id': version.id, 'updated_at': datetime.utcnow()}}
    )

    prompt.current_version_id = version.id
    logger.info(f"Prompt {prompt.id} created by {owner_id}")

    # Step 4: Return combined response
    return PromptResponse(
        id=str(prompt.id),
        owner_id=str(owner_id),
        name=prompt.name,
        description=prompt.description,
        tags=prompt.tags,
        prompt_metadata=prompt.metadata,
        current_version_id=str(version.id),
        created_at=prompt.created_at,
        updated_at=prompt.updated_at,
        current_version=PromptVersionResponse(
            id=str(version.id),
            prompt_id=str(prompt.id),
            version_number=version.version_number,
            version_name=version.version_name,
            content=version.content,
            changes_description=version.changes_description,
            created_at=version.created_at
        )
    )
