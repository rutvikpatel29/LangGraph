# main.py
# Entry point for running the agent supervisor workflow.

from .workflow import build_workflow
from .utils import save_graph_image, pretty_print_messages
from .config import GRAPH_IMAGE_PATH, TEST_QUERY

def run_supervisor_workflow(query: str = None):
    """Run the supervisor workflow with the given query."""
    if query is None:
        query = TEST_QUERY
    
    # Build and save the workflow
    supervisor = build_workflow()
    save_graph_image(supervisor, GRAPH_IMAGE_PATH)
    
    # Execute the workflow
    for chunk in supervisor.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        },
        subgraphs=True,
    ):
        pretty_print_messages(chunk, last_message=True)

if __name__ == "__main__":
    run_supervisor_workflow() 