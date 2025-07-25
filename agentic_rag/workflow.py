# workflow.py
# Constructs and compiles the agentic RAG workflow graph.

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from .nodes import generate_query_or_respond, grade_documents, rewrite_question, generate_answer


def build_workflow(MessagesState, retriever_tool, response_model):
    """
    Build and compile the workflow graph for the agentic RAG system.
    Nodes:
      - generate_query_or_respond: Decides to answer or retrieve
      - retrieve: Calls the retriever tool
      - rewrite_question: Rewrites the user question if needed
      - generate_answer: Generates the final answer
    """
    workflow = StateGraph(MessagesState)
    # Add nodes with unique names and bind required arguments using lambdas
    workflow.add_node("generate_query_or_respond", lambda state: generate_query_or_respond(state, response_model, retriever_tool))
    workflow.add_node("retrieve", ToolNode([retriever_tool]))
    workflow.add_node("rewrite_question", lambda state: rewrite_question(state, response_model))
    workflow.add_node("generate_answer", lambda state: generate_answer(state, response_model))
    # Start at query/response node
    workflow.add_edge(START, "generate_query_or_respond")
    # Decide whether to retrieve or end
    workflow.add_conditional_edges(
        "generate_query_or_respond",
        tools_condition,
        {
            "tools": "retrieve",
            END: END,
        },
    )
    # After retrieval, grade relevance and branch to rewrite or answer
    workflow.add_conditional_edges(
        "retrieve",
        grade_documents,
        {
            "rewrite_question": "rewrite_question",
            "generate_answer": "generate_answer"
        }
    )
    # End if answer is generated
    workflow.add_edge("generate_answer", END)
    # Loop back if question is rewritten
    workflow.add_edge("rewrite_question", "generate_query_or_respond")
    return workflow.compile() 