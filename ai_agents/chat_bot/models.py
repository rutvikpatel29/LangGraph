# models.py
# Model and tool initialization for the chat bot workflow.

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.types import interrupt

llm = ChatOpenAI(model='gpt-4o-mini')
tavily_tool = TavilySearch(max_results=2)

TOOLS = [tavily_tool] 