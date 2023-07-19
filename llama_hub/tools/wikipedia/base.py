"""Wikipedia tool spec."""

from llama_index.tools.tool_spec.base import BaseToolSpec
from llama_index.readers.schema.base import Document
from typing import Any, List


class WikipediaToolSpec(BaseToolSpec):
    """Wikipedia tool spec.

    Currently a simple wrapper around the data loader.

    """

    spec_functions = ["load_data", "search_data"]

    def load_data(
        self, pages: List[str], lang: str = "en", **load_kwargs: Any
    ) -> List[Document]:
        """Load data from wikipedia.

        Args:
            pages (List[str]): List of pages to read.
            lang  (str): language of wikipedia texts (default English)
        """
        import wikipedia
        from wikipedia import PageError

        try:
            results = []
            for page in pages:
                wikipedia.set_lang(lang)
                page_content = wikipedia.page(
                    page, **load_kwargs, auto_suggest=False
                ).content
                results.append(Document(text=page_content))
            return results
        except PageError:
            return "Unable to load page. Try searching instead."

    def search_data(self, query: str, lang: str = "en") -> List[Document]:
        """Searchs wikipedia for pages related to a query. Use this endpoint when load_data returns no results.

        Args:
            query (str): the string to search for
        """
        pages = wikipedia.search(query)
        if len(pages) == 0:
            return "Unable to find any details on this search"
        return self.load_data(pages, lang)
