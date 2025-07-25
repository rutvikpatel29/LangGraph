# workflow.py
# Constructs and compiles the chat bot workflow graph.

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from .nodes import chatbot, tool_node, route_tools, State

def build_workflow():
    graph = StateGraph(State)
    graph.add_node('chatbot', chatbot)
    graph.add_node('tools', tool_node)
    graph.add_edge(START, 'chatbot')
    graph.add_edge('chatbot', END)
    graph.add_conditional_edges('chatbot', route_tools, {'tools': 'tools', END: END})
    graph.add_edge('tools', 'chatbot')
    graph.add_edge(START, 'chatbot')
    memory = InMemorySaver()
    return graph.compile(checkpointer=memory) 