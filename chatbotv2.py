from langchain_community.llms.openai import OpenAI
from langchain_community.llms import Ollama
from langchain_neo4j import Neo4jGraph
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
import os

# Load environment variables
load_dotenv()

# Set up Neo4j connection
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URL"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

# Updated prompt template with node and relationship context
prompt_template = """
You are a helpful assistant for querying a graph database. The graph contains:
- Nodes of type `Student` with properties like `name,age,major`.
- Relationships such as `FRIENDS_WITH` connecting `Student` nodes.
- Relationships such as `ENROLLED_IN` linking a `Student` to their course.
- Nodes of type 'course' with properties like 'code,credits,name'.
-return the node and relationships of the nodes
# - Ensure the return only generates the properties of those node and ensure they have the friend prefix

A user will ask questions related to a graph, and you should generate a valid Cypher query accordingly.

User Query: {input}

Provide only the Cypher query, without any additional explanations:
"""

# Set up the LLM model (Ollama in this case)
prompt = PromptTemplate(input_variables=["input"], template=prompt_template)
llm = Ollama(model="ollama3.2")

# Create LLMChain to generate Cypher queries from user input
query_chain = LLMChain(prompt=prompt, llm=llm)

# Define a function for interacting with Neo4j and querying the graph
def query_graph(input_text: str):
    cypher_query = query_chain.run(input_text)  # Generate Cypher query using LLM
    print(f"Generated Cypher Query: {cypher_query}")  # Optionally, print the query for debugging
    # Query the Neo4j graph database using the generated Cypher query
    result = graph.query(cypher_query)  # Use the 'query' method to run the query
    return result

# Example user input
user_input = "Who are John Doe's friends and what are their majors?"

# Get the result
context = query_graph(user_input)
print(f"Context: {context}")
question="Who are John Doe friends and what are their majors"

question_prompt_template="""Answer the question based only on the context provided.

Question: {question}

Context: {context}

Answer like you are a professional chatbot

"""

question_prompt = PromptTemplate(input_variables=["question","context"], template=question_prompt_template)
question_answer_chain=LLMChain(prompt=question_prompt, llm=llm)
a= question_answer_chain.run({"question":question, "context":context})

print(a)
