import unittest
from unittest.mock import patch

import pytest
from llama_index.readers.schema.base import Document

from llama_hub.web.sitemap.base import SitemapReader

MOCK_URL = "https://gpt-index.readthedocs.io/sitemap.xml"


def get_sitemapdata():
    f = open("tests/tests_web_sitemap/test_sitemap.xml", "r")
    return f.read()


def dummy_load_pages(urls: str):
    documents = []
    for u in urls:
        doc = Document(text="Bla", extra_info={"Source": u})
        documents.append(doc)
    return documents


class TestSitemapReader(unittest.TestCase):
    def test_sitemap_reader_init(self):
        # test w/o args
        SitemapReader()

        # test w args
        SitemapReader(html_to_text=True, limit=50)

    def test_sitemap_reader_load_data_invalid_args(self):
        sitemap_reader = SitemapReader()

        with pytest.raises(
            TypeError,
            match="missing 1 required positional argument: 'sitemap_url'",
        ):
            sitemap_reader.load_data()

    @patch("llama_hub.web.async_web.base.AsyncWebPageReader.load_data")
    def test_sitemap_reader_load_data(self, mock_load_data):
        with patch("urllib.request.urlopen") as mock_urlopen:
            sitemap_reader = SitemapReader()

            # mock sitemap call
            mock_response = mock_urlopen.return_value
            mock_response.read.return_value = get_sitemapdata()

            mock_load_data.side_effect = dummy_load_pages

            documents = sitemap_reader.load_data(sitemap_url=MOCK_URL)

            mock_urlopen.assert_called_once_with(
                "https://gpt-index.readthedocs.io/sitemap.xml"
            )
            mock_response.read.assert_called_once()
            assert mock_load_data.call_count == 1
            assert len(documents) == 38

    @patch("llama_hub.web.async_web.base.AsyncWebPageReader.load_data")
    def test_sitemap_reader_load_data_with_filter(self, mock_load_data):
        with patch("urllib.request.urlopen") as mock_urlopen:
            sitemap_reader = SitemapReader()

            # mock sitemap call
            mock_response = mock_urlopen.return_value
            mock_response.read.return_value = get_sitemapdata()

            mock_load_data.side_effect = dummy_load_pages

            documents = sitemap_reader.load_data(
                sitemap_url=MOCK_URL,
                filter="https://gpt-index.readthedocs.io/en/latest/",
            )

            mock_urlopen.assert_called_once_with(
                "https://gpt-index.readthedocs.io/sitemap.xml"
            )
            mock_response.read.assert_called_once()
            assert mock_load_data.call_count == 1
            assert len(documents) == 1
            assert (
                documents[0].extra_info["Source"]
                == "https://gpt-index.readthedocs.io/en/latest/"
            )
