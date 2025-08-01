from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta, datetime
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from app.db.mongo import users_collection
from app.api.v1.auth.schemas import (
    UserCreate, UserLogin, Token, TokenRefreshRequest,
    PasswordResetRequest, PasswordReset
)
from app.core.security import (
    hash_password, verify_password, create_token, decode_token
)
from app.core.config import settings
from app.dependencies import rate_limit
from app.utils.email import send_email

router = APIRouter()


@router.post("/signup", summary="Create new user", dependencies=[Depends(rate_limit(times=5, seconds=5))])
async def signup(data: UserCreate):
    if data.password != data.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if await users_collection.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = await hash_password(data.password)
    user = {
        "email": data.email,
        "hashed_password": hashed,
        "is_verified": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    try:
        res = await users_collection.insert_one(user)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already registered (concurrent request)")

    token = await create_token({"user_id": str(res.inserted_id)})
    link = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    await send_email("Verify your email", data.email, f"Please verify your email: {link}")

    return {"message": "Signup successful. Check your email to verify your account."}

@router.post("/login", response_model=Token, summary="Authenticate user", dependencies=[Depends(rate_limit(times=5, seconds=10))])
async def login(data: UserLogin):
    user = await users_collection.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.get("is_verified"):
        raise HTTPException(status_code=403, detail="Email not verified")

    user_id = str(user["_id"])
    access = await create_token({"user_id": user_id}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh = await create_token({"user_id": user_id}, timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES))

    await users_collection.update_one(
        {"_id": user["_id"]}, {"$set": {"last_login_at": datetime.utcnow()}}
    )

    return {"access_token": access, "refresh_token": refresh}


@router.post("/refresh", response_model=Token, summary="Refresh access token")
async def refresh_token(req: TokenRefreshRequest):
    payload = await decode_token(req.refresh_token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    access = await create_token({"user_id": user_id}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh = await create_token({"user_id": user_id}, timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES))

    return {"access_token": access, "refresh_token": refresh}


@router.get("/verify-email", summary="Verify email")
async def verify_email(token: str):
    payload = await decode_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid token")

    res = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_verified": True}}
    )

    if res.modified_count != 1:
        raise HTTPException(status_code=400, detail="User not found or already verified")

    return {"message": "Email verified successfully."}


@router.post("/forgot-password", summary="Request password reset", dependencies=[Depends(rate_limit(times=5, seconds=60))])
async def forgot_password(req: PasswordResetRequest):
    user = await users_collection.find_one({"email": req.email})
    if user:
        token = await create_token({"user_id": str(user["_id"])})
        link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        await send_email("Reset your password", req.email, f"Reset your password using this link: {link}")

    return {"message": "If the email exists, a reset link has been sent."}


@router.post("/reset-password", summary="Reset password")
async def reset_password(req: PasswordReset):
    if req.new_password != req.new_password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if len(req.new_password) < 8 or not any(c.isdigit() for c in req.new_password):
        raise HTTPException(status_code=400, detail="Password too weak")

    payload = await decode_token(req.token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid token")

    hashed = await hash_password(req.new_password)
    res = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"hashed_password": hashed, "updated_at": datetime.utcnow()}}
    )

    if res.modified_count != 1:
        raise HTTPException(status_code=400, detail="Password not updated")

    return {"message": "Password has been reset."}
