# main.py
# Entry point for running the agentic RAG workflow and printing results.

from .data_loader import load_documents, split_documents, create_vectorstore
from .tools import get_retriever_tool
from .models import get_response_model
from .workflow import build_workflow
from .utils import save_graph_image
from langgraph.graph import MessagesState
from dotenv import load_dotenv

# Load environment variables (e.g., OpenAI API key)
load_dotenv()

if __name__ == "__main__":
    # Load and split documents
    docs_list = load_documents()
    doc_splits = split_documents(docs_list)
    # Create vector store and retriever
    vectorstore = create_vectorstore(doc_splits)
    retriever = vectorstore.as_retriever()
    retriever_tool = get_retriever_tool(retriever)
    # Initialize response model and build workflow graph
    response_model = get_response_model()
    graph = build_workflow(MessagesState, retriever_tool, response_model)
    # Save a visualization of the workflow graph
    save_graph_image(graph, "ai_agents/agentic_rag/graph.png")

    # Example user query
    input = {
        "messages": [
            {
                "role": "user",
                "content": "What does Lilian Weng say about types of reward hacking?",
            }
        ]
    }
    # Stream and print updates from the workflow
    for chunk in graph.stream(input):
        for node, update in chunk.items():
            print("Update from node", node)
            update["messages"][-1].pretty_print()
            print("\n\n") 