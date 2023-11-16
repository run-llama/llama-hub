import logging
import requests
import xmltodict
from typing import List

from llama_index import download_loader
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

logger = logging.getLogger(__name__)

class SitemapIndexReader(BaseReader):
    """Sitemap Index reader. Reads data from a sitemap index document.

    Args:
        html_to_text (bool): Whether to convert HTML to text.
            Requires `html2text` package.
        limit (int): Maximum number of concurrent requests.
    """
    def __init__(self, html_to_text: bool = False, limit: int = 10) -> None:
        """Initialize with parameters."""

        try:
            from llama_hub.utils import import_loader

            SitemapReader = import_loader("SitemapReader")
        except ImportError:
            SitemapReader = download_loader("SitemapReader")

        self._sitemap_loader = SitemapReader(html_to_text=html_to_text, limit=limit)
        self._html_to_text = html_to_text
        self._limit = limit


    def read_sitemap_urls(self, sitemap_index_url:str, sitemap_url_filters: list):
        sitemap_response = requests.get(sitemap_index_url)
        sitemap_index_dict = xmltodict.parse(sitemap_response.text)

        sitemap_entries = sitemap_index_dict['sitemapindex']['sitemap']
        logger.info("Found %s sitemap entries", len(sitemap_entries))

        sitemap_urls = []
        for sitemap_entry in sitemap_entries:
            if 'loc' not in sitemap_entry:
                logging.info("Skipping sitemap entry without loc: %s", sitemap_entry)
                continue
            loc = sitemap_entry['loc']
            if len(sitemap_url_filters) == 0 or any([url_filter in loc for url_filter in sitemap_url_filters]):
                logging.info("Adding sitemap entry with loc: %s", loc)
                sitemap_urls.append(loc)

        return sitemap_urls

    """
    Load data from a sitemap index document.
    
    Args:
        sitemap_index_url (str): URL of the sitemap index document.
        sitemap_url_filters (list): List of URL filters to select sitemap urls from the index. Defaults to empty list.
    """
    def load_data(self, sitemap_index_url: str, sitemap_url_filters: list = []) -> List[Document]:
        sitemap_urls = self.read_sitemap_urls(sitemap_index_url, sitemap_url_filters)
        sitemap_index_documents = []
        for url in sitemap_urls:
            sitemap_documents = self._sitemap_loader.load_data(sitemap_url=url)
            logging.info("Loaded %s documents from %s", len(sitemap_documents), url)
            sitemap_index_documents.extend(sitemap_documents)
        return sitemap_index_documents
