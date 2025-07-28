from typing import List, Dict, Optional, Union, Mapping
from collections import Counter
from datetime import timedelta, datetime


class EvaluationService:
    def evaluate_response(self, llm_resp: str, prompt: str, metrics: List[str]) -> Dict[str, Union[float, str]]:
        scores: dict = {}
        keywords = prompt.split()[:5]
        for m in metrics:
            if m == "keywords_present":
                count = sum(1 for kw in keywords if kw in llm_resp)
                scores[m] = count / len(keywords)
            elif m == "output_length":
                scores[m] = len(llm_resp)
            elif m in ("relevance", "coherence"):
                scores[m] = "N/A"  # placeholder
        return scores

    def compare_llm_outputs(self, o1: str, o2: str, criteria: List[str]) -> Dict[str, Dict]:
        results: dict = {}
        for c in criteria:
            if c == "length_difference":
                results[c] = {"o1": len(o1), "o2": len(o2), "difference": abs(len(o1) - len(o2))}
            elif c == "common_phrases":
                bi1 = set(o1.split())
                bi2 = set(o2.split())
                common = list(bi1 & bi2)
                results[c] = {"common_phrases": common[:10]}
        return results
