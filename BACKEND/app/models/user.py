from enum import Enum
from pydantic import BaseModel, EmailStr
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from beanie import Document


class User(Document):
    email: str
    hashed_password: str
    is_verified: bool: bool = False

    # 🔥 Admin access
    is_admin: bool: bool = False

    class Settings:
        name = "users"


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserDB(BaseModel):
    id: ObjectId = await Field(..., alias="_id")
    email: EmailStr
    hashed_password: str
    role: UserRole = UserRole.USER
    is_active: bool = True
    is_verified: bool: bool = False
    created_at: datetime = await Field(default_factory=datetime.utcnow)
    updated_at: datetime = await Field(default_factory=datetime.utcnow)


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserInDB(BaseModel):
    id: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_verified: bool: bool = False
    role: UserRole = UserRole.USER
    # other fields...
