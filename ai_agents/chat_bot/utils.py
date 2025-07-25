# utils.py
# Utility functions for the chat bot project.

def save_graph_image(graph, path: str):
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png()) 