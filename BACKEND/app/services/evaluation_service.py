# app/services/evaluation_service.py

from typing import List, Dict

class EvaluationService:
    async def evaluate_response(
        self, generated_output: str, input_prompt: str, metrics: List[str]
    ) -> Dict[str, float]:
        """
        Evaluate a single LLM response based on selected metrics.
        """
        result = {}
        for metric in metrics:
            if metric == "length":
                result["length"] = len(generated_output)
            elif metric == "contains_prompt":
                result["contains_prompt"] = float(input_prompt in generated_output)
            elif metric == "word_count":
                result["word_count"] = len(generated_output.strip().split())
            # Add more metrics as needed
            else:
                result[metric] = -1.0  # Unknown metric
        return result

    async def compare_llm_outputs(
        self, output1: str, output2: str, criteria: List[str]
    ) -> Dict[str, float]:
        """
        Compare two LLM responses based on given criteria.
        """
        result = {}
        for criterion in criteria:
            if criterion == "length_diff":
                result["length_diff"] = abs(len(output1) - len(output2))
            elif criterion == "same_output":
                result["same_output"] = float(output1.strip() == output2.strip())
            elif criterion == "word_count_diff":
                wc1 = len(output1.strip().split())
                wc2 = len(output2.strip().split())
                result["word_count_diff"] = abs(wc1 - wc2)
            # Add more criteria as needed
            else:
                result[criterion] = -1.0  # Unknown criterion
        return result
