from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.prompts.prompt import PromptTemplate

load_dotenv()

NEO4J_URL = os.getenv("NEO4J_URL")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
LLM_BASE_URL=os.getenv("LLM_BASE_URL")
LLM_API_KEY=os.getenv("LLM_API_KEY")


llm=ChatOpenAI(base_url=LLM_BASE_URL,temperature=0.8,streaming=True,api_key=LLM_API_KEY)
