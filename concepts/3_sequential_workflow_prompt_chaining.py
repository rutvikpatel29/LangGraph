from typing import TypedDict
from langchain_community.chat_models import ChatOllama
from langgraph.graph import StateGraph, START, END

# create a model
model = ChatOllama(model="llama3.2")

class BlogState(TypedDict):

    title: str
    outline: str
    content: str

def create_outline(state: BlogState) -> BlogState:
    # fetch title
    title = state['title']
    # call llm gen outline
    prompt = f'Generate a detailed outline for a blog on the topic - {title}'
    outline = model.invoke(prompt).content
    # update state
    state['outline'] = outline

    return state


def create_blog(state: BlogState) -> BlogState:
    title = state['title']
    outline = state['outline']
    prompt = f'Write a detailed blog on the title - {title} using the follwing outline \n {outline}'
    content = model.invoke(prompt).content
    state['content'] = content

    return state

graph = StateGraph(BlogState)

# nodes
graph.add_node('create_outline', create_outline)
graph.add_node('create_blog', create_blog)

# edges
graph.add_edge(START, 'create_outline')
graph.add_edge('create_outline', 'create_blog')
graph.add_edge('create_blog', END)

workflow = graph.compile()

# visualize the graph
def save_graph_image(graph, path: str):
    with open(path, "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png())
save_graph_image(workflow, "concepts/graph.png")

# execute
intial_state = {'title': 'Rise of AI in India'}
final_state = workflow.invoke(intial_state)
print(final_state['content'])