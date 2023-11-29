import urllib.request
import xml.etree.ElementTree as ET

from llama_index import download_loader
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


XML_SITEMAP_SCHEMA = "http://www.sitemaps.org/schemas/sitemap/0.9"
STRIPE_SITEMAP_URL = "https://stripe.com/sitemap/sitemap.xml"

DEFAULT_FILTERS = ["/docs"]


class StripeDocsReader(BaseReader):
    """Asynchronous Stripe documentation reader.

    Reads pages from the Stripe documentation based on the sitemap.xml.

    Args:
        html_to_text (bool): Whether to convert HTML to text.
        limit (int): Maximum number of concurrent requests.
    """

    def __init__(self, html_to_text: bool = False, limit: int = 10) -> None:
        try:
            from llama_hub.utils import import_loader

            AsyncWebPageReader = import_loader("AsyncWebPageReader")
        except ImportError:
            AsyncWebPageReader = download_loader("AsyncWebPageReader")

        self._async_loader = AsyncWebPageReader(html_to_text=html_to_text, limit=limit)
        self._html_to_text = html_to_text
        self._limit = limit

    def _load_url(self, url: str) -> str:
        url_request = urllib.request.urlopen(url)

        return url_request.read()

    def _load_sitemap(self) -> str:
        return self._load_url(STRIPE_SITEMAP_URL)

    def _parse_sitemap(
        self, raw_sitemap: str, filters: list[str] = DEFAULT_FILTERS
    ) -> list:
        root_sitemap = ET.fromstring(raw_sitemap)
        sitemap_partition_urls = []
        sitemap_urls = []

        for sitemap in root_sitemap.findall(f"{{{XML_SITEMAP_SCHEMA}}}sitemap"):
            loc = sitemap.find(f"{{{XML_SITEMAP_SCHEMA}}}loc").text
            sitemap_partition_urls.append(loc)

        for sitemap_partition_url in sitemap_partition_urls:
            urls = self._load_url(sitemap_partition_url).split(" ")

            for url in urls:
                contains_filter = any(filter in url for filter in filters)

                if contains_filter:
                    sitemap.append(url)

        return sitemap_urls

    def load_data(self, filters: list[str] = DEFAULT_FILTERS) -> list[Document]:
        sitemap = self._load_sitemap()
        sitemap_urls = self._parse_sitemap(sitemap, filters)

        return self._async_loader.load_data(urls=sitemap_urls)
