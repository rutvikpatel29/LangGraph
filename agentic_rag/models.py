# models.py
# Handles model initialization for the agentic_rag project.

from langchain.chat_models import init_chat_model


def get_response_model():
    """Initialize the main response model (OpenAI GPT-4.1)."""
    return init_chat_model("openai:gpt-4.1", temperature=0)


def get_grader_model():
    """Initialize the grader model (OpenAI GPT-4.1)."""
    return init_chat_model("openai:gpt-4.1", temperature=0) 