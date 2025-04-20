from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from dotenv import load_dotenv
import os
from llm import llm
from graph import graph
from langchain.prompts.prompt import PromptTemplate


CYPHER_GENERATION_TEMPLATE = """
You are an expert Neo4j Developer translating user questions into Cypher to answer questions about students, courses, and country.
Convert the user's question based on the schema.
- Nodes of type `Student` with properties like `Name,Age,Major,Id`.
- Node of type `Course` with properties like `Id, Name,Tutor`.
- Node of type `County` with properties like `Code, Name`.

- Relationships such as `FRIENDS_WITH` connecting `Student` nodes.
- Relationships such as `IS_FROM` connecting `Student` nodes to country of origin or where students are from.
- Relationships such as `ENROLLED_IN` linking a `Student` to the courses they are enrolled in.

Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Ensure the query includes only **one** `RETURN` clause,Do **not** include multiple relationship types (like `ENROLLED_IN` and `IS_FROM`) unless they are related in a single query context

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

