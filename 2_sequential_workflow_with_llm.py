from typing import TypedDict
from langchain_community.chat_models import ChatOllama
from langgraph.graph import StateGraph, START, END

# create a model
model = ChatOllama(model="llama3.2")

# create a state
class LLMState(TypedDict):
    question: str
    answer: str

def llm_qa(state: LLMState) -> LLMState:
    # extract the question from state
    question = state['question']
    # form a prompt
    prompt = f'Answer the following question {question}'
    # ask that question to the LLM
    answer = model.invoke(prompt).content
    # update the answer in the state
    state['answer'] = answer

    return state

# create our graph
graph = StateGraph(LLMState)

# add nodes
graph.add_node('llm_qa', llm_qa)

# add edges
graph.add_edge(START, 'llm_qa')
graph.add_edge('llm_qa', END)

# compile
workflow = graph.compile()

# visualize the graph
def save_graph_image(graph, path: str):
    with open(path, "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png())
save_graph_image(workflow, "LangGraph/graph.png")

# execute
intial_state = {'question': 'How far is moon from the earth?'}
final_state = workflow.invoke(intial_state)
print(final_state['answer'])
