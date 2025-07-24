from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition

from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

# --- Environment Setup ---
load_dotenv()

# --- Type Definitions ---
class State(TypedDict):
    messages: Annotated[list, add_messages]

# --- Tool Definitions ---
@tool
def get_stock_price(symbol: str) -> float:
    '''Return the current price of a stock given the stock symbol'''
    return {
        "MSFT": 200.3,
        "AAPL": 100.4,
        "AMZN": 150.0,
        "RIL": 87.6
    }.get(symbol, 0.0)

tools = [get_stock_price]

# --- LLM Initialization ---
llm = init_chat_model("llama3.2", model_provider="ollama")
llm_with_tools = llm.bind_tools(tools)

# --- Node Functions ---
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# --- Graph Construction ---
def build_graph():
    builder = StateGraph(State)
    builder.add_node("chatbot", chatbot)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "chatbot")
    builder.add_conditional_edges("chatbot", tools_condition)
    builder.add_edge("tools", "chatbot")
    return builder.compile(checkpointer=memory)


def save_graph_image(graph, path: str):
    with open(path, "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png())

# --- Main Execution ---
if __name__ == "__main__":
    graph = build_graph()
    save_graph_image(graph, "LangGraph/graph.png")

    config1 = { 'configurable': { 'thread_id': '1'} }

    msg = "I want to buy 20 AMZN stocks using current price. Then 15 MSFT. What will be the total cost?"
    state = graph.invoke({"messages": [{"role": "user", "content": msg}]}, config=config1)
    print(state["messages"][-1].content)


    config2 = { 'configurable': { 'thread_id': '2'} }

    msg = "Tell me the current price of 5 AAPL stocks."

    state = graph.invoke({"messages": [{"role": "user", "content": msg}]}, config=config2)
    print(state["messages"][-1].content)


    msg = "Using the current price tell me the total price of 10 RIL stocks and add it to previous total cost"

    state = graph.invoke({"messages": [{"role": "user", "content": msg}]}, config=config1)
    print(state["messages"][-1].content)


    msg = "Tell me the current price of 5 MSFT stocks and add it to previous total"

    state = graph.invoke({"messages": [{"role": "user", "content": msg}]}, config=config2)
    print(state["messages"][-1].content)


