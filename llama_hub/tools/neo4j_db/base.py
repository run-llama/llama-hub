from llama_index import Document
from llama_index.graph_stores import Neo4jGraphStore
from llama_index.tools.tool_spec.base import BaseToolSpec
from llama_index.llms.base import LLM, ChatMessage


class Neo4jQueryToolSpec(BaseToolSpec):
    """
    This class is responsible for querying a Neo4j graph database based on a provided schema definition.
    """

    def __init__(self, url, user, password, database, llm: LLM):
        """
        Initializes the Neo4jSchemaWiseQuery object.

        Args:
            url (str): The connection string for the Neo4j database.
            user (str): Username for the Neo4j database.
            password (str): Password for the Neo4j database.
            llm (obj): A language model for generating Cypher queries.
        """
        try:
            from neo4j import GraphDatabase

        except ImportError:
            raise ImportError(
                "`neo4j` package not found, please run `pip install neo4j`"
            )

        self.graph_store = Neo4jGraphStore(url=url, username=user, password=password, database=database)
        self.llm = llm

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
        {self.graph_store.schema}

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
        with self.graph_store.client.session() as session:
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
        with self.graph_store.client.session() as session:
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
            ChatMessage(role='system', content=self.get_system_message()),
            ChatMessage(role='user', content=question),
        ]
        # Used for Cypher healing flows
        if history:
            messages.extend(history)

        completions = self.llm.chat(messages)
        return completions.message.content

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
        from neo4j.exceptions import CypherSyntaxError

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
                    ChatMessage(role='assistant', content=cypher),
                    ChatMessage(role='system', conent=f"""This query returns an error: {str(e)} 
                        Give me a improved query that works without any explanations or apologies"""),
                ],
                retry=False
            )