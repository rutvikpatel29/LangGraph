# models.py
# Model initialization and schema definitions for the tweeter post generator workflow.

from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from .config import GENERATOR_MODEL, EVALUATOR_MODEL, OPTIMIZER_MODEL
from pydantic import BaseModel, Field
from typing import Literal

from dotenv import load_dotenv
load_dotenv()


# LLMs

generator_llm = ChatOllama(model=GENERATOR_MODEL)
evaluator_llm = ChatOpenAI(model=EVALUATOR_MODEL)
optimizer_llm = ChatOpenAI(model=OPTIMIZER_MODEL)

# Pydantic schema for evaluation
class TweetEvaluation(BaseModel):
    evaluation: Literal["approved", "needs_improvement"] = Field(..., description="Final evaluation result.")
    feedback: str = Field(..., description="feedback for the tweet.") 