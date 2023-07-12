"""Google Search tool spec."""

from llama_index.tools.tool_spec.base import BaseToolSpec
from llama_index.readers.schema.base import Document
import requests
import urllib.parse

QUERY_URL_TMPL = (
    "https://www.googleapis.com/customsearch/v1?key={key}&cx={engine}&q={query}"
)


class GoogleSearchToolSpec(BaseToolSpec):
    """Google Search tool spec."""

    spec_functions = ["google_search"]

    def __init__(self, key: str, engine: str) -> Document:
        """Initialize with parameters."""
        self.key = key
        self.engine = engine

    def google_search(self, query: str):
        """
        Make a query the google search engine to receive a list of results.

        Args:
            query (str): The query to be passed to google search.

        """
        response = requests.get(
            QUERY_URL_TMPL.format(
                key=self.key, engine=self.engine, query=urllib.parse.quote_plus(query)
            )
        )
        return [Document(text=response.text)]
