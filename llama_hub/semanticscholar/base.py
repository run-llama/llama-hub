import logging
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
import requests
from typing import List


class SemanticScholarReader(BaseReader):
    """
    A class to read and process data from Semantic Scholar API
    ...

    Methods
    -------
    __init__():
       Instantiate the SemanticScholar object

    load_data(query: str, limit: int = 10, returned_fields: list = ["title", "abstract", "venue", "year", "paperId", "citationCount", "openAccessPdf", "authors"]) -> list:
        Loads data from Semantic Scholar based on the query and returned_fields

    """

    def __init__(self):
        """
        Instantiate the SemanticScholar object
        """
        from semanticscholar import SemanticScholar

        self.s2 = SemanticScholar()

    def load_data(
        self,
        query,
        limit=10,
        returned_fields=[
            "title",
            "abstract",
            "venue",
            "year",
            "paperId",
            "citationCount",
            "openAccessPdf",
            "authors",
        ],
    ) -> List[Document]:
        """
        Loads data from Semantic Scholar based on the entered query and returned_fields

        Parameters
        ----------
        query: str
            The search query for the paper
        limit: int, optional
            The number of maximum results returned (default is 10)
        returned_fields: list, optional
            The list of fields to be returned from the search

        Returns
        -------
        list
            The list of Document object that contains the search results

        Raises
        ------
        Exception
            If there is an error while performing the search

        """
        try:
            results = self.s2.search_paper(query, limit=limit, fields=returned_fields)
        except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as e:
            logging.error(
                "Failed to fetch data from Semantic Scholar with exception: %s", e
            )
            raise
        except Exception as e:
            logging.error("An unexpected error occurred: %s", e)
            raise

        documents = []

        for item in results[:limit]:
            openaccesspdf = getattr(item, "openAccessPdf", None)
            abstract = getattr(item, "abstract", None)
            title = getattr(item, "title", None)
            text = None
            # concat title and abstract
            if abstract and title:
                text = title + " " + abstract
            elif not abstract:
                text = title

            metadata = {
                "title": title,
                "venue": getattr(item, "venue", None),
                "year": getattr(item, "year", None),
                "paperId": getattr(item, "paperId", None),
                "citationCount": getattr(item, "citationCount", None),
                "openAccessPdf": openaccesspdf.get("url") if openaccesspdf else None,
                "authors": [author["name"] for author in getattr(item, "authors", [])],
            }
            documents.append(Document(text=text, extra_info=metadata))

        return documents
