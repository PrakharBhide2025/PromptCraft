# PromptCraft 🚀

**PromptCraft** is an LLM-powered toolkit for optimizing, version-controlling, and evaluating developer prompts used in code generation, debugging, and technical documentation tasks.

## Key Features

-  **Prompt Versioning**: Seamless GitHub integration for tracking and managing prompt history.
-  **Prompt Evaluation**: Built-in evaluation system for comparing LLM outputs across OpenAI & HuggingFace APIs.
-  **Advanced Prompt Engineering**: Templates and patterns for generating reliable AI responses.
-  **Analytics Dashboard**: Track usage, output stability, and prompt performance.

## Impact

- Improved LLM prompt reliability by **50%**
- Reduced debugging time for developers
- Increased adoption of internal AI tooling

## Tech Stack

- **Frontend**: React.js / Streamlit
- **Backend**: FastAPI, MongoDB
- **LLMs**: OpenAI API, HuggingFace
- **DevOps**: Docker, GitHub OAuth, REST APIs

## Setup Instructions

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
