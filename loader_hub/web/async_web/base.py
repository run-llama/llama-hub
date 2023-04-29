import asyncio
from typing import List

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class AsyncWebPageReader(BaseReader):
    """Asynchronous web page reader.

    Reads pages from the web asynchronously.

    Args:
        html_to_text (bool): Whether to convert HTML to text.
            Requires `html2text` package.
        limit (int): Maximum number of concurrent requests.

    """

    def __init__(self, html_to_text: bool = False, limit: int = 10) -> None:
        """Initialize with parameters."""
        try:
            import html2text  # noqa: F401
        except ImportError:
            raise ImportError(
                "`html2text` package not found, please run `pip install html2text`"
            )
        try:
            import aiohttp  # noqa: F401
        except ImportError:
            raise ImportError(
                "`aiohttp` package not found, please run `pip install aiohttp`"
            )
        self._limit = limit
        self._html_to_text = html_to_text

    def load_data(self, urls: List[str]) -> List[Document]:
        """Load data from the input urls.

        Args:
            urls (List[str]): List of URLs to scrape.

        Returns:
            List[Document]: List of documents.

        """
        import aiohttp

        def chunked_http_client(limit: int):
            semaphore = asyncio.Semaphore(limit)

            async def http_get(url: str, session: aiohttp.ClientSession):
                async with semaphore:
                    async with session.get(url) as response:
                        return await response.text()

            return http_get

        async def fetch_urls(urls: List[str]):
            http_client = chunked_http_client(self._limit)
            async with aiohttp.ClientSession() as session:
                tasks = [http_client(url, session) for url in urls]
                return await asyncio.gather(*tasks, return_exceptions=True)

        if not isinstance(urls, list):
            raise ValueError("urls must be a list of strings.")

        documents = []
        responses = asyncio.run(fetch_urls(urls))
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                raise ValueError(f"One of the inputs is not a valid url: {urls[i]}")
            if self._html_to_text:
                import html2text

                response = html2text.html2text(response)

            documents.append(Document(response))

        return documents
