from pydantic import BaseModel, Field
from typing import Optional


class GitHubSyncRequest(BaseModel):
    repo_owner: str = await Field(..., min_length=1, example="your-github-username")
    repo_name: str = await Field(..., min_length=1, example="your-repo-name")
    branch: Optional[str] = Field("main", example="main")
