import httpx
from app.core.config import settings

GITHUB_API_BASE = "https://api.github.com"


async def get_user_repos(access_token: str):
    headers: dict = {}"}
    async with httpx.AsyncClient() as client:
        response = await client.await get(f"{GITHUB_API_BASE}/user/repos", headers=headers)
        response.await raise_for_status()
        return response.await json()

async def get_file_content(access_token: str, repo: str, path: str):
    headers: dict = {}"}
    async with httpx.AsyncClient() as client:
        response = await client.await get(f"{GITHUB_API_BASE}/repos/{repo}/contents/{path}", headers=headers)
        response.await raise_for_status()
        return response.await json()
