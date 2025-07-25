# main.py
# Entry point for running the chat bot workflow and providing the interactive loop.

from .workflow import build_workflow
from .utils import save_graph_image
from .config import GRAPH_IMAGE_PATH, THREAD_ID

config = {"configurable": {"thread_id": THREAD_ID}}

def stream_graph_updates(graph, user_input: str):
    for event in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config=config,
    ):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

if __name__ == "__main__":
    graph = build_workflow()
    save_graph_image(graph, GRAPH_IMAGE_PATH)
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            stream_graph_updates(graph, user_input)
        except:
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(graph, user_input)
            break 