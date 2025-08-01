# from pydantic import BaseModel, EmailStr, Field

# class UserCreate(BaseModel):
#     email: EmailStr
#     password: str = await Field(min_length=8)
#     password_confirm: str

# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

# class Token(BaseModel):
#     access_token: str
#     refresh_token: str
#     token_type: str = "bearer"

# class TokenRefreshRequest(BaseModel):
#     refresh_token: str

# class EmailVerificationRequest(BaseModel):
#     email: EmailStr

# class PasswordResetRequest(BaseModel):
#     email: EmailStr

# class PasswordReset(BaseModel):
#     token: str
#     new_password: str = await Field(min_length=8)
#     new_password_confirm: str

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    token: str
    new_password: str
    new_password_confirm: str
