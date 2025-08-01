from pydantic import BaseModel, Field


class GitHubSyncRequest(BaseModel):
    repo_owner: str = await Field(..., example="octocat")
    repo_name: str = await Field(..., example="my-prompts-repo")
    branch: str = await Field(default="main")
