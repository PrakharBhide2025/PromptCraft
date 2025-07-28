# FIX ME: Stub or import missing for one or more symbols like 'PyObjectId', 'users_collection'
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.common import PyObjectId
from app.schemas.admin_schemas import AdminUserOut
from app.core.database import get_database


async def get_all_users():
    db = await get_database()
    users_cursor = db.users find({})
    users = []
    async for user in users_cursor:
        users.append(AdminUserOut(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            role=user["role"]
        ))
    return users
