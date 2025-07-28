from typing import Union
from pydantic import BaseModel
from typing import List, Dict, Union
from typing_extensions import Literal
from typing import Optional  # Add this import
from typing import Optional, Union, Mapping

class EvaluationRequest(BaseModel):
    llm_response_log_id: str
    metrics: List[Literal["relevance", "coherence",
                          "keywords_present", "output_length"]]


class EvaluationResultResponse(BaseModel):
    llm_response_log_id: str
    scores: Dict[str, Union[float, str]]
    evaluation_notes: Optional[str] = None


class LLMComparisonRequest(BaseModel):
    llm_response_log_id_1: str
    llm_response_log_id_2: str
    comparison_criteria: List[Literal["length_difference", "common_phrases"]]


class LLMComparisonResponse(BaseModel):
    llm_response_log_id_1: str
    llm_response_log_id_2: str
    comparison_results: Dict[str, Dict]
