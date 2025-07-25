# tools.py
# Defines retriever tool creation for the agentic_rag project.

from langchain.tools.retriever import create_retriever_tool


def get_retriever_tool(retriever):
    """Create a retriever tool for searching blog posts."""
    return create_retriever_tool(
        retriever,
        "retrieve_blog_posts",
        "Search and return information about Lilian Weng blog posts."
    ) 