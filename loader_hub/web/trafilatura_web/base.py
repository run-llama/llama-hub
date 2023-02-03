from typing import List

from gpt_index.readers.base import BaseReader
from gpt_index.readers.schema.base import Document


class TrafilaturaWebReader(BaseReader):
    """Trafilatura web page reader.

    Reads pages from the web.
    Requires the `trafilatura` package.

    """

    def __init__(self) -> None:
        """Initialize with parameters."""
        try:
            import trafilatura  # noqa: F401
        except ImportError:
            raise ValueError(
                "`trafilatura` package not found, please run `pip install trafilatura`"
            )

    def load_data(self, urls: List[str]) -> List[Document]:
        """Load data from the urls.

        Args:
            urls (List[str]): List of URLs to scrape.

        Returns:
            List[Document]: List of documents.

        """
        import trafilatura

        if not isinstance(urls, list):
            raise ValueError("urls must be a list of strings.")
        documents = []
        for url in urls:
            downloaded = trafilatura.fetch_url(url)
            response = trafilatura.extract(downloaded)
            documents.append(Document(response))

        return documents
