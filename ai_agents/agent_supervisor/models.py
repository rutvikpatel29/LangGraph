# models.py
# Model and tool initialization for the agent supervisor workflow.

from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from .config import MODEL_NAME, TAVILY_MAX_RESULTS

load_dotenv()

# Initialize web search tool
web_search = TavilySearch(max_results=TAVILY_MAX_RESULTS) 