from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# --- Environment Setup ---
load_dotenv()

# --- Type Definitions ---
class State(TypedDict):
    messages: Annotated[list, add_messages]

# --- LLM Initialization ---
llm = init_chat_model("llama3.2", model_provider="ollama")

# --- Node Functions ---
def chatbot(state: State) -> State:
    return {"messages": [llm.invoke(state["messages"])]}

# --- Graph Construction ---
def build_graph():
    builder = StateGraph(State)
    builder.add_node("chatbot_node", chatbot)
    builder.add_edge(START, "chatbot_node")
    builder.add_edge("chatbot_node", END)
    return builder.compile()

def save_graph_image(graph, path: str):
    with open(path, "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png())

# --- Main Execution ---
if __name__ == "__main__":
    graph = build_graph()
    save_graph_image(graph, "LangGraph/graph.png")

    # Example message
    message = {"role": "user", "content": "Who walked on the moon for the first time? Print only the name"}
    response = graph.invoke({"messages": [message]})
    print("Bot:", response["messages"][0].content)

    # Interactive chat loop
    state = None
    while True:
        in_message = input("You: ")
        if in_message.lower() in {"quit", "exit"}:
            break
        if state is None:
            state = {"messages": [{"role": "user", "content": in_message}]}
        else:
            state["messages"].append({"role": "user", "content": in_message})
        state = graph.invoke(state)
        print("Bot:", state["messages"][-1].content)