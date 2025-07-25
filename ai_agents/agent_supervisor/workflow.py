# workflow.py
# Constructs and compiles the agent supervisor workflow graph.

from langgraph.graph import StateGraph, START, MessagesState
from .agents import research_agent, math_agent, supervisor_agent_with_description

def build_workflow():
    """Build and compile the supervisor workflow graph."""
    supervisor_with_description = (
        StateGraph(MessagesState)
        .add_node(
            supervisor_agent_with_description, destinations=("research_agent", "math_agent")
        )
        .add_node(research_agent)
        .add_node(math_agent)
        .add_edge(START, "supervisor")
        .add_edge("research_agent", "supervisor")
        .add_edge("math_agent", "supervisor")
        .compile()
    )
    return supervisor_with_description 