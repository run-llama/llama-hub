"""monday.com reader."""
from typing import List

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
import json
import requests

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
        data = self.perform_request(query)
        return [Document(f"{data}", extra_info={})]

    def perform_request(query: str):
        """Fetch GraphQL data"""


        headers = {"Authorization" : self.api_key}
        data = {'query' : query}

        response = requests.post(url=self.api_url, json=data, headers=headers)
        json_response = r.json()
        
        return json_response