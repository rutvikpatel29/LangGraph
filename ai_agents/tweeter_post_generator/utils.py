# utils.py
# Utility functions for the tweeter post generator project.

def save_graph_image(graph, path: str):
    """Save a visualization of the workflow graph as a PNG image."""
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png()) 