# workflow.py
# Constructs and compiles the tweeter post generator workflow graph.

from langgraph.graph import StateGraph, START, END
from .nodes import generate_tweet, evaluate_tweet, optimize_tweet, route_evaluation, TweetState

def build_workflow():
    graph = StateGraph(TweetState)
    graph.add_node('generate', generate_tweet)
    graph.add_node('evaluate', evaluate_tweet)
    graph.add_node('optimize', optimize_tweet)
    graph.add_edge(START, 'generate')
    graph.add_edge('generate', 'evaluate')
    graph.add_conditional_edges('evaluate', route_evaluation, {'approved': END, 'needs_improvement': 'optimize'})
    graph.add_edge('optimize', 'evaluate')
    return graph.compile() 