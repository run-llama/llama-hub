"""GraphQL Tool."""

from typing import Optional

from llama_index.tools.tool_spec.base import BaseToolSpec
import requests

class GraphQLToolSpec(BaseToolSpec):
    """Requests Tool"""

    spec_functions = ["graphql_request"]

    def __init__(self, url: str, headers: Optional[dict] = {}):
        self.headers = headers
        self.url = url

    def graphql_request(self, query: str, variables: str, operationName: str):
        """
        Use this tool to make a GraphQL query against the server.

        Args:
            query (str): The GraphQL query to execute
            variables (str): The variable values for the query
            operationName (str): The name for the query

        example input:
            "query":"query Ships {\n  ships {\n    id\n    model\n    name\n    type\n    status\n  }\n}",
            "variables":{},
            "operationName":"Ships"

        """
        res = requests.post(self.url, headers=self.headers, json={
            'query': query,
            'variables': variables,
            'operationName': operationName
        })
        return res.text

