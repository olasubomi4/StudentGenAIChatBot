from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

NEO4J_URL = os.getenv("NEO4J_URL")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
LLM_BASE_URL=os.getenv("LLM_BASE_URL")
LLM_API_KEY=os.getenv("LLM_API_KEY")


llm=ChatOpenAI(base_url=LLM_BASE_URL,temperature=0.3,streaming=True,api_key=LLM_API_KEY)
