# main.py
# Entry point for running the tweeter post generator workflow and printing results.

from .workflow import build_workflow
from .utils import save_graph_image
from .config import GRAPH_IMAGE_PATH

if __name__ == "__main__":
    workflow = build_workflow()
    save_graph_image(workflow, GRAPH_IMAGE_PATH)

    initial_state = {
        "topic": "srhberhb",
        "iteration": 1,
        "max_iteration": 2
    }

    result = workflow.invoke(initial_state)
    print('Final State:')
    print(result)
    print('\nTweet history:')
    for tweet in result['tweet_history']:
        print(tweet) 