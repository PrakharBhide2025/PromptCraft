# # app/schemas/prompt_schema.py

# from pydantic import BaseModel
# from typing import List, Optional, Dict, Any

# class PromptSchema(BaseModel):
#     input_text: str
#     purpose: str
#     name: Optional[str] = None
#     description: Optional[str] = None
#     tags: List[str] = []
#     prompt_metadata: Dict[str, Any] = {}

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class PromptSchema(BaseModel):
    input_text: str
    purpose: str
    name: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    prompt_metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        schema_extra = {
            "example": {
                "input_text": "Explain quicksort algorithm.",
                "purpose": "generate_output",
                "name": "Quicksort prompt",
                "description": "A prompt to get explanation of quicksort",
                "tags": ["sorting", "algorithms"],
                "prompt_metadata": {"difficulty": "medium"}
            }
        }

