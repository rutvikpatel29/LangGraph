# utils.py
# Utility functions for the customer review reply project.

def save_graph_image(graph, path: str):
    """Save a visualization of the workflow graph as a PNG image."""
    with open(path, "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png()) 