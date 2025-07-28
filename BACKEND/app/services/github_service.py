import httpx
import logging
import yaml
import json
import base64
from app.core.config import settings

logger = logging.getLogger(__name__)

async def get_file_content(token, owner, repo, path, branch="main") -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params={})
        resp.raise_for_status()
        data = resp.json()
    
    return base64.b64decode(data["content"]).decode("utf-8")

def parse_prompt_file(raw: str) -> dict:
    """
    Parses YAML front matter and content.
    """
    parts = raw.split("---")
    meta = yaml.safe_load(parts[1])
    content = "---".join(parts[2:])
    
    return {
        "name": meta["name"],
        "tags": meta.get("tags", []),
        "metadata": {k: v for k, v in meta.items() if k not in ["name", "tags"]},
        "content": content
    }
