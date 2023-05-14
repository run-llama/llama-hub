"""monday.com reader."""
from typing import List

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
import json
import requests
from graphql.parser import GraphQLParser

class MondayReader(BaseReader):
    """monday.com reader. Reads data by a GraphQL query.

    Args:
        api_key (str): monday.com API key.
    """
    
    def __init__(self, api_key: str) -> None:
        """Initialize monday.com reader."""
        
        self.api_key = api_key
        self.api_url = "https://api.monday.com/v2"

    def load_data(self, query: str) -> List[Document]:
        """Load data by a graphQL query

        Args:
            query (str): GraphQL query.
        Returns:
            List[Document]: List of documents.
        """

        headers = {"Authorization" : self.api_key}
        data = {'query' : query}

        response = requests.post(url=self.api_url, json=data, headers=headers)
        json_response = response.json()

        response_data = json_response['data']

        parser = GraphQLParser()
        parsed_quert = parser.parse(query)
        query_object_name = parsed_quert.definitions[0].selections[0].name

        return [Document(f"{response_data[query_object_name]}", extra_info={})]