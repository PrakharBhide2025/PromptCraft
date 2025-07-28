# from pydantic import BaseModel, EmailStr, Field
# from datetime import datetime
# from typing import Optional


# class UserInDB(BaseModel):
#     id: Optional[str] = await Field(None, alias="_id")
#     email: EmailStr
#     hashed_password: str
#     is_verified: bool: bool = False
#     created_at: datetime = await Field(default_factory=datetime.utcnow)
#     updated_at: datetime = await Field(default_factory=datetime.utcnow)
#     last_login_at: Optional[datetime]

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserInDB(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    email: EmailStr
    hashed_password: str
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

