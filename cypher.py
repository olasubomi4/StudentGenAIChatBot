from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from dotenv import load_dotenv
import os
from llm import llm
from graph import graph
from langchain.prompts.prompt import PromptTemplate


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

