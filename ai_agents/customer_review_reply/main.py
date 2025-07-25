# main.py
# Entry point for running the customer review reply workflow and printing results.

from .workflow import build_workflow
from .utils import save_graph_image
from .config import GRAPH_IMAGE_PATH
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    graph = build_workflow()
    save_graph_image(graph, GRAPH_IMAGE_PATH)

    intial_state = {
        'review': "I’ve been trying to log in for over an hour now, and the app keeps freezing on the authentication screen. I even tried reinstalling it, but no luck. This kind of bug is unacceptable, especially when it affects basic functionality."
    }
    final_state = graph.invoke(intial_state)
    print('Final State:')
    print(final_state)
    print('\nGenerated Response:')
    print(final_state.get('response', 'No response generated')) 