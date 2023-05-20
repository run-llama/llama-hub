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

    def parse_item_values(self, cv):
        data = {}
        data["id"]= cv["id"]
        data["name"]= cv["title"]
        data["value"]= cv["text"]

        return data

    def parse_data(self, item):
        data = {}
        data["id"] = item["id"]
        data["name"] = item["name"]
        data["values"] = list(map(self.parse_item_values, list(item["column_values"])))

        return data

    def load_data(self, board_id: int) -> List[Document]:
        """Load board data by board_id

        Args:
            board_id (int): monday.com board id.
        Returns:
            List[Document]: List of items as documents.
            [{id, name, values: [{id, name, value}]}]
        """

        headers = {"Authorization" : self.api_key}
        query = """
            query{
                boards(ids: [%d]){
                    items{
                        id,
                        name,
                        column_values{
                            id,
                            title,
                            text
                        }
                    }
                }
            } """ % (board_id)
        data = {'query' : query}

        response = requests.post(url=self.api_url, json=data, headers=headers)
        json_response = response.json()

        items_array = list(json_response['data']['boards'][0]["items"])
        result = map(self.parse_data, list(items_array))

        return [Document(list(result), extra_info={})]