from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from llama_index import Document
from neo4j import GraphDatabase
from neo4j.exceptions import CypherSyntaxError

node_properties_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE NOT type = "RELATIONSHIP" AND elementType = "node"
WITH label AS nodeLabels, collect(property) AS properties
RETURN {labels: nodeLabels, properties: properties} AS output

"""

rel_properties_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE NOT type = "RELATIONSHIP" AND elementType = "relationship"
WITH label AS nodeLabels, collect(property) AS properties
RETURN {type: nodeLabels, properties: properties} AS output
"""

rel_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE type = "RELATIONSHIP" AND elementType = "node"
RETURN {source: label, relationship: property, target: other} AS output
"""


def schema_text(node_props, rel_props, rels):
    return f"""
  This is the schema representation of the Neo4j database.
  Node properties are the following:
  {node_props}
  Relationship properties are the following:
  {rel_props}
  Relationship point from source to target nodes
  {rels}
  Make sure to respect relationship types and directions
  """


class Neo4jQueryToolSpec:
    """
    This class is responsible for querying a Neo4j graph database based on a provided schema definition.
    """

    def __init__(self, url, user, password, llm):
        """
        Initializes the Neo4jSchemaWiseQuery object.

        Args:
            url (str): The connection string for the Neo4j database.
            user (str): Username for the Neo4j database.
            password (str): Password for the Neo4j database.
            llm (obj): A language model for generating Cypher queries.
        """
        self.driver = GraphDatabase.driver(url, auth=(user, password))
        # construct schema
        self.schema = self.generate_schema()
        self.llm = llm

    def generate_schema(self):
        """
        Generates a schema based on the Neo4j database.

        Returns:
            str: The generated schema.
        """
        node_props = self.query_graph_db(node_properties_query)
        rel_props = self.query_graph_db(rel_properties_query)
        rels = self.query_graph_db(rel_query)
        return schema_text(node_props, rel_props, rels)

    def refresh_schema(self):
        self.schema = self.generate_schema()

    def get_system_message(self):
        """
        Generates a system message detailing the task and schema.

        Returns:
            str: The system message.
        """
        return f"""
        Task: Generate Cypher queries to query a Neo4j graph database based on the provided schema definition.
        Instructions:
        Use only the provided relationship types and properties.
        Do not use any other relationship types or properties that are not provided.
        If you cannot generate a Cypher statement based on the provided schema, explain the reason to the user.
        Schema:
        {self.schema}

        Note: Do not include any explanations or apologies in your responses.
        """

    def query_graph_db(self, neo4j_query, params=None):
        """
        Queries the Neo4j database.

        Args:
            neo4j_query (str): The Cypher query to be executed.
            params (dict, optional): Parameters for the Cypher query. Defaults to None.

        Returns:
            list: The query results.
        """
        if params is None:
            params = {}
        with self.driver.session() as session:
            result = session.run(neo4j_query, params)
            output = [r.values() for r in result]
            output.insert(0, list(result.keys()))
            return output

    def query_graph_db_as_document(self, neo4j_query, params=None):
        """
        Queries the Neo4j database.

        Args:
            neo4j_query (str): The Cypher query to be executed.
            params (dict, optional): Parameters for the Cypher query. Defaults to None.

        Returns:
            list: The query results.
        """
        if params is None:
            params = {}
        with self.driver.session() as session:
            result = session.run(neo4j_query, params)
            output = [Document(text="\n".join([f"{key}:{val}" for key, val in zip(r.keys(), r.values())])) for r in result]
            return output

    def construct_cypher_query(self, question, history=None):
        """
        Constructs a Cypher query based on a given question and history.

        Args:
            question (str): The question to construct the Cypher query for.
            history (list, optional): A list of previous interactions for context. Defaults to None.

        Returns:
            str: The constructed Cypher query.
        """
        messages = [
            SystemMessage(content=self.get_system_message()),
            HumanMessage(content=question),
        ]
        # Used for Cypher healing flows
        if history:
            messages.extend(history)

        completions = self.llm(messages)
        return completions.content

    def run(self, question, history=None, retry=True):
        """
        Executes a Cypher query based on a given question.

        Args:
            question (str): The question to execute the Cypher query for.
            history (list, optional): A list of previous interactions for context. Defaults to None.
            retry (bool, optional): Whether to retry in case of a syntax error. Defaults to True.

        Returns:
            list/str: The query results or an error message.
        """
        # Construct Cypher statement
        cypher = self.construct_cypher_query(question, history)
        print(cypher)
        try:
            return self.query_graph_db_as_document(cypher)
        # Self-healing flow
        except CypherSyntaxError as e:
            # If out of retries
            if not retry:
                return "Invalid Cypher syntax"
            # Self-healing Cypher flow by
            # providing specific error to GPT-4
            print("Retrying")
            return self.run(
                question,
                [
                    AIMessage(content=cypher),
                    SystemMessage(conent=f"""This query returns an error: {str(e)} 
                        Give me a improved query that works without any explanations or apologies"""),
                ],
                retry=False
            )
