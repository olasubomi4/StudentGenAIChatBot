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

if not all([NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD]):
    raise ValueError("Missing one or more required environment variables for Neo4j connection.")

graph = Neo4jGraph(url=NEO4J_URL, username=NEO4J_USERNAME, password=NEO4J_PASSWORD,enhanced_schema=True)

llm=ChatOpenAI(base_url=LLM_BASE_URL,temperature=0.8,streaming=True,api_key=LLM_API_KEY)



CYPHER_GENERATION_TEMPLATE = """
You are an expert Neo4j Developer translating user questions into Cypher to answer questions about students and courses.
Convert the user's question based on the schema.
- Nodes of type `Student` with properties like `name,age,major`.
- Relationships such as `FRIENDS_WITH` connecting `Student` nodes.
- Relationships such as `ENROLLED_IN` linking a `Student` to their course.

Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Do not return entire nodes or embedding properties.

Fine Tuning:

Schema:
{schema}

Question:
{question}

Cypher Query:
"""

cypher_prompt = PromptTemplate.from_template(CYPHER_GENERATION_TEMPLATE)
cypher_chain = GraphCypherQAChain.from_llm(
   llm, graph=graph, verbose=True,  cypher_prompt=cypher_prompt,
    allow_dangerous_requests=True,function_response_system="Respond like you are smart"
)

a=cypher_chain.invoke(
    "How many courses are John doe enrolled in"
)

print(a)
