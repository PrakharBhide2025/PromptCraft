from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
import httpx
from app.core.config import settings

router = APIRouter(tags=["GitHub"])  


@router.get("/github/login")
async def github_login():
    github_oauth_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&redirect_uri={settings.FRONTEND_URL}/oauth/callback"
        f"&scope=repo,user"
    )
    return RedirectResponse(github_oauth_url)  


@router.get("/github/callback")
async def github_callback(code: str):
    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            },
        )

        token_res.raise_for_status()  # ✅ Fixed typo (`raise_for_status` is a method)
        token_json = token_res.json()
        access_token = token_json.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="GitHub token exchange failed")

        return {"access_token": access_token}
