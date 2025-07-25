# nodes.py
# Node functions for the customer review reply workflow.

from .models import model, SentimentSchema, DiagnosisSchema
from typing import TypedDict, Literal

# State definition for the workflow
class ReviewState(TypedDict):
    review: str
    sentiment: Literal["positive", "negative"]
    diagnosis: dict
    response: str

def find_sentiment(state: ReviewState):
    """Find the sentiment of the review using the LLM."""
    prompt = f'For the following review find out the sentiment \n {state["review"]}'
    structured_model = model.with_structured_output(SentimentSchema)
    sentiment = structured_model.invoke(prompt).sentiment
    return {'sentiment': sentiment}

def check_sentiment(state: ReviewState) -> Literal["positive_response", "run_diagnosis"]:
    """Route based on sentiment."""
    if state['sentiment'] == 'positive':
        return 'positive_response'
    else:
        return 'run_diagnosis'

def positive_response(state: ReviewState):
    """Generate a thank-you message for positive reviews."""
    prompt = f"""Write a warm thank-you message in response to this review:\n\n\"{state['review']}\"\nAlso, kindly ask the user to leave feedback on our website."""
    response = model.invoke(prompt).content
    return {'response': response}

def run_diagnosis(state: ReviewState):
    """Diagnose the negative review using the LLM."""
    prompt = f"""Diagnose this negative review:\n\n{state['review']}\nReturn issue_type, tone, and urgency."""
    structured_model2 = model.with_structured_output(DiagnosisSchema)
    response = structured_model2.invoke(prompt)
    return {'diagnosis': response.model_dump()}

def negative_response(state: ReviewState):
    """Generate an empathetic, helpful resolution message for negative reviews."""
    diagnosis = state['diagnosis']
    prompt = f"""You are a support assistant.\nThe user had a '{diagnosis['issue_type']}' issue, sounded '{diagnosis['tone']}', and marked urgency as '{diagnosis['urgency']}'.\nWrite an empathetic, helpful resolution message."""
    response = model.invoke(prompt).content
    return {'response': response} 