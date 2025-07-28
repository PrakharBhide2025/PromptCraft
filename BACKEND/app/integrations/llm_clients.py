# from abc import ABC, abstractmethod
# from typing import Dict
# from openai import AsyncOpenAI  # ✅ Import new client
# import httpx


# class BaseLLMClient(ABC):
#     @abstractmethod
#     async def generate_text(self, prompt_content: str, model_name: str, **kwargs) -> Dict:
#         pass


# class OpenAIClient(BaseLLMClient):
#     def __init__(self, api_key: str):
#         if not api_key:
#             raise ValueError("OpenAI API key is missing")
#         self.client = AsyncOpenAI(api_key=api_key)  # ✅ Pass api_key here

#     async def generate_text(self, prompt_content: str, model_name: str, **kwargs) -> Dict:
#         try:
#             resp = await self.client.chat.completions.create(
#                 model=model_name,
#                 messages=[{"role": "user", "content": prompt_content}],
#                 **kwargs
#             )
#             usage = resp.usage.to_dict()
#             return {
#                 "text": resp.choices[0].message.content,
#                 "prompt_tokens": usage["prompt_tokens"],
#                 "completion_tokens": usage["completion_tokens"],
#                 "total_tokens": usage["total_tokens"],
#             }
#         except Exception as e:
#             raise RuntimeError(f"OpenAI failure: {e}")

# class HuggingFaceClient(BaseLLMClient):
#     def __init__(self, api_token: str, endpoint: str):
#         self.api_token = api_token
#         self.endpoint = endpoint

#     async def generate_text(self, prompt_content: str, model_name: str, **kwargs) -> Dict:
#         headers: dict = {
#             "Authorization": f"Bearer {self.api_token}",
#             "Content-Type": "application/json"
#         }

#         payload: dict = {
#             "inputs": prompt_content,
#             "parameters": kwargs,
#         }

#         async with httpx.AsyncClient() as client:
#             try:
#                 resp = await client.post(self.endpoint, json=payload, headers=headers)
#                 resp.raise_for_status()
#                 data = resp.json()

#                 # If response is a list (like many HF inference APIs return), handle accordingly
#                 if isinstance(data, list):
#                     data = data[0]

#                 return {
#                     "text": data.get("generated_text", ""),
#                     "prompt_tokens": data.get("prompt_tokens", 0),
#                     "completion_tokens": data.get("completion_tokens", 0),
#                     "total_tokens": data.get("prompt_tokens", 0) + data.get("completion_tokens", 0),
#                 }
#             except Exception as e:
#                 raise RuntimeError(f"HuggingFace failure: {e}")


# def get_llm_client(provider: str, **cfg) -> BaseLLMClient:
#     if provider == "openai":
#         return OpenAIClient(api_key=cfg["openai_api_key"])
#     elif provider == "huggingface":
#         return HuggingFaceClient(api_token=cfg["hf_api_token"], endpoint=cfg["hf_endpoint"])
#     else:
#         raise ValueError(f"Unsupported LLM provider: {provider}")


from abc import ABC, abstractmethod
from typing import Dict
from openai import AsyncOpenAI
import httpx
import os
from dotenv import load_dotenv

# ✅ Load environment variables at module load
load_dotenv()


class BaseLLMClient(ABC):
    @abstractmethod
    async def generate_text(self, prompt_content: str, model_name: str, **kwargs) -> Dict:
        pass


class OpenAIClient(BaseLLMClient):
    def __init__(self, api_key: str = None):
        # ✅ Fallback to env var if not passed
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is missing")
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def generate_text(self, prompt_content: str, model_name: str, **kwargs) -> Dict:
        try:
            resp = await self.client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt_content}],
                **kwargs
            )
            usage = resp.usage.to_dict()
            return {
                "text": resp.choices[0].message.content,
                "prompt_tokens": usage["prompt_tokens"],
                "completion_tokens": usage["completion_tokens"],
                "total_tokens": usage["total_tokens"],
            }
        except Exception as e:
            raise RuntimeError(f"OpenAI failure: {e}")


class HuggingFaceClient(BaseLLMClient):
    def __init__(self, api_token: str = None, endpoint: str = None):
        # ✅ Fallback to env vars if not passed
        self.api_token = api_token or os.getenv("HF_TOKEN")
        self.endpoint = endpoint or os.getenv("HF_ENDPOINT")
        if not self.api_token or not self.endpoint:
            raise ValueError("Hugging Face token or endpoint is missing")

    async def generate_text(self, prompt_content: str, model_name: str, **kwargs) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": prompt_content,
            "parameters": kwargs,
        }

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(self.endpoint, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()

                if isinstance(data, list):  # e.g., HF returns [{generated_text: "..."}]
                    data = data[0]

                return {
                    "text": data.get("generated_text", ""),
                    "prompt_tokens": data.get("prompt_tokens", 0),
                    "completion_tokens": data.get("completion_tokens", 0),
                    "total_tokens": data.get("prompt_tokens", 0) + data.get("completion_tokens", 0),
                }
            except Exception as e:
                raise RuntimeError(f"HuggingFace failure: {e}")


def get_llm_client(provider: str, **cfg) -> BaseLLMClient:
    if provider == "openai":
        return OpenAIClient(api_key=cfg.get("openai_api_key"))
    elif provider == "huggingface":
        return HuggingFaceClient(
            api_token=cfg.get("hf_api_token"),
            endpoint=cfg.get("hf_endpoint")
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

