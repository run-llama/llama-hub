"""Metaphor tool spec."""

from llama_index.tools.tool_spec.base import BaseToolSpec
from llama_index.readers.schema.base import Document
from typing import Optional, Any


class MetaphorToolSpec(BaseToolSpec):
    """Metaphor tool spec."""

    spec_functions = ["search", "find_similar", "get_contents"]

    def __init__(self, api_key: str) -> None:
        """Initialize with parameters."""
        from metaphor_python import Metaphor
        
        self._api_key = api_key
        self.client = Metaphor(api_key)

    def search(
        self, query: str, **kwargs: Any
    ):
        """
        This function performs a search on the Metaphor API.

        Args:
            query (str): The search query.
            num_results (int, optional): The number of search results to return.
            include_domains (list, optional): A list of domains to include in the search.
            exclude_domains (list, optional): A list of domains to exclude from the search.
            start_crawl_date (str, optional): The start date for the crawl (in YYYY-MM-DD format).
            end_crawl_date (str, optional): The end date for the crawl (in YYYY-MM-DD format).
            start_published_date (str, optional): The start date for when the document was published (in YYYY-MM-DD format).
            end_published_date (str, optional): The end date for when the document was published (in YYYY-MM-DD format).
            use_autoprompt (bool, optional): Whether to use autoprompt for the search.
            type (str, optional): The type of search to perform, "neural" or "keyword". Default: "neural"

        Raises:
            ValueError: If the 'num' is not an integer between 1 and 10.
        """
        return self.client.search(query, **kwargs)

    def find_similar(
        url: str, **kwargs: Any
    ) -> Any:
        """This function performs a similarity search using a base url.

        Args:
            url (str): The base url to find similar links to.
            num_results (int, optional): The number of search results to return.
            include_domains (list, optional): A list of domains to include in the search.
            exclude_domains (list, optional): A list of domains to exclude from the search.
            start_crawl_date (str, optional): The start date for the crawl (in YYYY-MM-DD format).
            end_crawl_date (str, optional): The end date for the crawl (in YYYY-MM-DD format).
            start_published_date (str, optional): The start date for when the document was published (in YYYY-MM-DD format).
            end_published_date (str, optional): The end date for when the document was published (in YYYY-MM-DD format).
        
        """
        return self.client.find_similar(url, **kwargs)