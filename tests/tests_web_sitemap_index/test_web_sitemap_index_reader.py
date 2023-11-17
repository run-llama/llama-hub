import unittest
from unittest.mock import patch, Mock

import pytest
from llama_index.readers.schema.base import Document
from llama_hub.web.sitemap_index.base import SitemapIndexReader
import requests

MOCK_SITEMAP_INDEX_URL = "https://gpt-index.readthedocs.io/sitemap_index.xml"

SITEMAP_URL_REGION_MAP = {
    "https://gpt-index.readthedocs.io/en/sitemap.xml": "EN",
    "https://gpt-index.readthedocs.io/fr/sitemap.xml": "FR",
    "https://gpt-index.readthedocs.io/jp/sitemap.xml": "JP"
}

SITE_URLS = [
    "https://gpt-index.readthedocs.io/{region}/stable/",
    "https://gpt-index.readthedocs.io/{region}/latest/",
    "https://gpt-index.readthedocs.io/{region}/stable/quickstart/"]

def get_sitemap_index_data():
    f = open("tests/tests_web_sitemap_index/test_sitemap_index.xml", "r")
    return f.read()

def dummy_load_pages(sitemap_url: str):
    region = SITEMAP_URL_REGION_MAP[sitemap_url]
    urls = [url.format(region=region) for url in SITE_URLS]
    documents = []
    for url in urls:
        doc = Document(text=f"Sample text in region: {region} for url: {url}", extra_info={"Source": url})
        documents.append(doc)
    return documents


class TestSitemapIndexReader(unittest.TestCase):
    def test_sitemap_index_reader_init(self):
        # test w/o args
        SitemapIndexReader()

        # test w args
        SitemapIndexReader(html_to_text=True, limit=50)

    def test_sitemap_reader_load_data_invalid_args(self):
        sitemap_index_reader = SitemapIndexReader()

        with pytest.raises(
            TypeError,
            match="missing 1 required positional argument: 'sitemap_index_url'",
        ):
            sitemap_index_reader.load_data()

    @patch("llama_hub.web.sitemap.base.SitemapReader.load_data")
    def test_sitemap_index_reader_load_data(self, mock_load_data):
        with patch("requests.get") as mock_requests_get:
            sitemap_index_reader = SitemapIndexReader()

            # mock sitemap call
            mock_response = requests.Response()
            mock_response.headers['Content-Type'] = 'text/plain'
            mock_response._content = get_sitemap_index_data().encode('utf-8')
            mock_response.status_code = 200
            mock_requests_get.return_value = mock_response

            mock_load_data.side_effect = dummy_load_pages

            documents = sitemap_index_reader.load_data(sitemap_index_url=MOCK_SITEMAP_INDEX_URL)

            mock_requests_get.assert_called_once_with(MOCK_SITEMAP_INDEX_URL)
            assert mock_load_data.call_count == 3
            assert len(documents) == 9

    @patch("llama_hub.web.sitemap.base.SitemapReader.load_data")
    def test_sitemap_index_reader_load_data_with_filter(self, mock_load_data):
        with patch("requests.get") as mock_requests_get:
            sitemap_index_reader = SitemapIndexReader()

            # mock sitemap call
            mock_response = requests.Response()
            mock_response.headers['Content-Type'] = 'text/plain'
            mock_response._content = get_sitemap_index_data().encode('utf-8')
            mock_response.status_code = 200
            mock_requests_get.return_value = mock_response

            mock_load_data.side_effect = dummy_load_pages

            documents = sitemap_index_reader.load_data(
                sitemap_index_url=MOCK_SITEMAP_INDEX_URL,
                sitemap_url_filters=["en", "fr"])

            mock_requests_get.assert_called_once_with(MOCK_SITEMAP_INDEX_URL)
            assert mock_load_data.call_count == 2
            assert len(documents) == 6
