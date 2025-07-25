# workflow.py
# Constructs and compiles the customer review reply workflow graph.

from langgraph.graph import StateGraph, START, END
from .nodes import find_sentiment, check_sentiment, positive_response, run_diagnosis, negative_response, ReviewState

def build_workflow():
    """Build and compile the workflow graph for the customer review reply system."""
    graph = StateGraph(ReviewState)
    graph.add_node('find_sentiment', find_sentiment)
    graph.add_node('positive_response', positive_response)
    graph.add_node('run_diagnosis', run_diagnosis)
    graph.add_node('negative_response', negative_response)
    graph.add_edge(START, 'find_sentiment')
    graph.add_conditional_edges('find_sentiment', check_sentiment)
    graph.add_edge('positive_response', END)
    graph.add_edge('run_diagnosis', 'negative_response')
    graph.add_edge('negative_response', END)
    return graph.compile() 