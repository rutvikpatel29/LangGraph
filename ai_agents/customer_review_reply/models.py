# models.py
# Model initialization and schema definitions for the customer review reply workflow.

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Literal
from .config import MODEL_NAME
from dotenv import load_dotenv
load_dotenv()

# Initialize the main chat model
model = ChatOpenAI(model=MODEL_NAME)

# Pydantic schemas for structured outputs
class SentimentSchema(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(description='Sentiment of the review')

class DiagnosisSchema(BaseModel):
    issue_type: Literal["UX", "Performance", "Bug", "Support", "Other"] = Field(description='The category of issue mentioned in the review')
    tone: Literal["angry", "frustrated", "disappointed", "calm"] = Field(description='The emotional tone expressed by the user')
    urgency: Literal["low", "medium", "high"] = Field(description='How urgent or critical the issue appears to be') 