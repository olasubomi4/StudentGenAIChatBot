
from langchain_community.llms import Ollama
from langchain_neo4j import Neo4jGraph
from dotenv import load_dotenv
import os

load_dotenv()
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URL"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

query = """
MATCH (s:Student)-[:FRIENDS_WITH]->(friend)
WHERE s.name = $student_name
RETURN friend.name AS friendsName, friend.major AS friendsMajor
"""

params = {"student_name": "John Doe"}
results = graph.query(query, params)

context=results
llm = Ollama(model="llama3.2")
question="Who are John Doe friends and what are their majors"

prompt=f"""Answer the question based only on the context provided.

Question: {question}

Context: {context}

"""

response = llm.invoke(input=prompt)
print(response)
