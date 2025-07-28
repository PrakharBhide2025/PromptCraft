from pydantic import BaseModel
from typing import Dict, Any

class GenerateLLMRequest(BaseModel):
    prompt_id: str
    model_name: str
    provider: str
    llm_parameters: Dict[str, Any]

    class Config:
        schema_extra = {
            "example": {
                "prompt_id": "abc123",
                "model_name": "gpt-3.5-turbo",
                "provider": "openai",
                "llm_parameters": {
                    "temperature": 0.7,
                    "max_tokens": 300
                }
            }
        }